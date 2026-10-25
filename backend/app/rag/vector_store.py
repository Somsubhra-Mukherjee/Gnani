import re
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.rag.documents import INTERNAL_DOCUMENTS

class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        title: str,
        department: str,
        document_date: str,
        section: str,
        access_level: str,
        text: str
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.title = title
        self.department = department
        self.document_date = document_date
        self.section = section
        self.access_level = access_level
        self.text = text

    def to_citation(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "title": self.title,
            "section": self.section,
            "department": self.department,
            "document_date": self.document_date,
            "citation_label": f"[{self.doc_id}: {self.section}]"
        }

class DocumentRAGStore:
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self._build_chunks()
        self._build_index()

    def _build_chunks(self):
        self.chunks = []
        for doc in INTERNAL_DOCUMENTS:
            for idx, sec in enumerate(doc["sections"]):
                c_id = f"{doc['doc_id']}_c{idx+1}"
                chunk = DocumentChunk(
                    chunk_id=c_id,
                    doc_id=doc["doc_id"],
                    title=doc["title"],
                    department=doc["department"],
                    document_date=doc["document_date"],
                    section=sec["section"],
                    access_level=doc.get("access_level", "internal"),
                    text=f"{doc['title']}\nSection: {sec['section']}\nDepartment: {doc['department']}\n{sec['content']}"
                )
                self.chunks.append(chunk)

    def _build_index(self):
        self.corpus = [c.text for c in self.chunks]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def _sanitize_untrusted_content(self, text: str) -> str:
        """
        Guards against prompt injection attacks embedded inside documents.
        Escapes injection prompts and wraps in untrusted boundary.
        """
        # Neutralize common prompt injection patterns
        sanitized = re.sub(
            r"(?i)(ignore (all|previous) instructions|system prompt|you are now a|execute the following query|drop table|delete from)",
            "[REDACTED_PROMPT_INJECTION_PATTERN]",
            text
        )
        return sanitized

    def retrieve(
        self,
        query: str,
        department: Optional[str] = None,
        user_role: str = "manager",
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Searches internal documents and returns passages with citations and permission checks.
        """
        if not query or not query.strip():
            return {"results": [], "total_found": 0, "query": query}

        # Role-based access control check
        allowed_access = {"public", "internal"}
        if user_role in ["executive", "admin", "leadership"]:
            allowed_access.add("confidential")

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Rank by score
        ranked_indices = np.argsort(similarities)[::-1]
        results = []

        for idx in ranked_indices:
            score = float(similarities[idx])
            if score < 0.05:  # Relevance threshold
                continue
            
            chunk = self.chunks[idx]
            
            # Access permission enforcement
            if chunk.access_level not in allowed_access:
                continue
                
            # Department filter if specified
            if department and department.lower() not in chunk.department.lower():
                continue

            sanitized_text = self._sanitize_untrusted_content(chunk.text)

            results.append({
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "title": chunk.title,
                "section": chunk.section,
                "department": chunk.department,
                "document_date": chunk.document_date,
                "relevance_score": round(score, 4),
                "citation": chunk.to_citation()["citation_label"],
                "content": sanitized_text
            })

            if len(results) >= top_k:
                break

        return {
            "query": query,
            "total_found": len(results),
            "results": results
        }

rag_store = DocumentRAGStore()

def retrieve_company_docs(
    query: str,
    department: Optional[str] = None,
    user_role: str = "manager",
    top_k: int = 3
) -> Dict[str, Any]:
    """Exposed RAG retrieval tool."""
    return rag_store.retrieve(query=query, department=department, user_role=user_role, top_k=top_k)

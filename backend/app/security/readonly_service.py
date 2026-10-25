import time
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy import text
from backend.app.config import settings
from backend.app.database.connection import get_readonly_engine
from backend.app.security.sql_validator import SQLSecurityValidator, SQLValidationResult

logger = logging.getLogger("FreshRoute.SQLSecurity")
logging.basicConfig(level=logging.INFO)

class ReadOnlyQueryService:
    def __init__(self):
        self.validator = SQLSecurityValidator(
            max_row_limit=settings.SQL_MAX_ROW_LIMIT,
            dialect="sqlite" if settings.DATABASE_URL.startswith("sqlite") else "postgres"
        )
        self.engine = get_readonly_engine()
        self.timeout_seconds = settings.SQL_QUERY_TIMEOUT_SECONDS

    def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        business_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validates and executes a read-only SQL query against the company database.
        Returns sanitized results, timing metadata, and security audit information.
        """
        start_time = time.time()
        params = parameters or {}
        
        # 1. AST Validation
        val_result: SQLValidationResult = self.validator.validate(query)
        if not val_result.is_valid:
            logger.warning(
                f"[SECURITY AUDIT - REJECTED] Context: '{business_context}' | "
                f"Query: {query[:120]}... | Reason: {val_result.error}"
            )
            return {
                "success": False,
                "error": f"Security Validation Rejected: {val_result.error}",
                "query_submitted": query,
                "sanitized_query": None,
                "rows": [],
                "row_count": 0,
                "columns": [],
                "duration_ms": round((time.time() - start_time) * 1000, 2),
                "business_context": business_context,
                "tables_accessed": []
            }

        executable_sql = val_result.sanitized_query or query

        # 2. Trusted Read-Only Execution with Timeout
        try:
            with self.engine.connect() as conn:
                # For SQLite, enforce PRAGMA query_only=ON for defense-in-depth
                if settings.DATABASE_URL.startswith("sqlite"):
                    conn.execute(text("PRAGMA query_only = ON;"))
                
                # Execute parameterized query
                result = conn.execute(text(executable_sql), params)
                columns = list(result.keys()) if result.returns_rows else []
                raw_rows = result.fetchmany(self.validator.max_row_limit) if result.returns_rows else []
                
                # Convert rows to serializable dicts
                rows = [dict(zip(columns, row)) for row in raw_rows]
                duration_ms = round((time.time() - start_time) * 1000, 2)

                logger.info(
                    f"[SECURITY AUDIT - EXECUTED] Context: '{business_context}' | "
                    f"Tables: {val_result.tables_accessed} | Rows: {len(rows)} | Duration: {duration_ms}ms"
                )

                return {
                    "success": True,
                    "error": None,
                    "query_submitted": query,
                    "sanitized_query": executable_sql,
                    "rows": rows,
                    "row_count": len(rows),
                    "columns": columns,
                    "duration_ms": duration_ms,
                    "business_context": business_context,
                    "tables_accessed": val_result.tables_accessed
                }

        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(
                f"[SECURITY AUDIT - DB ERROR] Context: '{business_context}' | "
                f"Query: {executable_sql[:120]}... | Error: {str(e)}"
            )
            return {
                "success": False,
                "error": f"Database Execution Error: {str(e)}",
                "query_submitted": query,
                "sanitized_query": executable_sql,
                "rows": [],
                "row_count": 0,
                "columns": [],
                "duration_ms": duration_ms,
                "business_context": business_context,
                "tables_accessed": val_result.tables_accessed
            }

readonly_query_service = ReadOnlyQueryService()

def run_readonly_sql(
    query: str,
    parameters: Optional[Dict[str, Any]] = None,
    business_context: Optional[str] = None
) -> Dict[str, Any]:
    """Exposed tool callable by agent orchestrator."""
    return readonly_query_service.execute_query(query, parameters, business_context)

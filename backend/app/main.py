import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.config import settings
from backend.app.database.schema import init_db
from backend.app.api.routes_chat import router as chat_router
from backend.app.api.routes_voice import router as voice_router
from backend.app.api.routes_workspace import router as workspace_router

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Secure Voice-First AI Business Intelligence Agent for Great Indian AI Internship Challenge 2026",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(chat_router)
app.include_router(voice_router)
app.include_router(workspace_router)

# Mount frontend build if it exists
frontend_dist_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.exists(frontend_dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_dir, "assets")), name="assets")

    @app.get("/")
    def serve_frontend_index():
        return FileResponse(os.path.join(frontend_dist_dir, "index.html"))

@app.on_event("startup")
def on_startup():
    # Ensure database tables and views exist
    init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "database": "sqlite/freshroute.db (Read-Only Enforced)",
        "gnani_models": {
            "stt": settings.GNANI_STT_MODEL,
            "tts": settings.GNANI_TTS_MODEL,
            "llm": settings.GNANI_LLM_MODEL
        },
        "security_policy": "Strict AST SQL Validation (No writes, no stacked queries, whitelisted tables only)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

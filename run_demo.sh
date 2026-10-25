#!/usr/bin/env bash
set -e

echo "=========================================================================="
echo " FreshRoute AI: Voice-First BI Agent (Gnani.ai Challenge 2026)"
echo "=========================================================================="

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required."
    exit 1
fi

# Ensure data directory and database exists
if [ ! -f "backend/data/freshroute.db" ]; then
    echo "==> Seeding FreshRoute synthetic database (seed=42)..."
    PYTHONPATH=. python3 backend/app/database/seed_data.py
else
    echo "==> Verified database exists at backend/data/freshroute.db"
fi

# Run quality checks
echo "==> Running data quality checks..."
PYTHONPATH=. python3 backend/app/database/data_quality.py

# Check if frontend build exists
if [ ! -d "frontend/dist" ]; then
    echo "==> Building frontend distribution bundle..."
    cd frontend && npm run build && cd ..
fi

echo "=========================================================================="
echo " Starting FastAPI Server on http://localhost:8000"
echo " Interactive Workspace:  http://localhost:8000"
echo " API Docs:               http://localhost:8000/docs"
echo "=========================================================================="
PYTHONPATH=. python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

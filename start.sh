#!/bin/bash
# Start script for Render

echo "Starting FastAPI server..."
cd backend
uvicorn api.fastapi_app:app --host 0.0.0.0 --port ${PORT:-8000}

"""StreamForge — Production Hardening Workspace

Pre-built FastAPI application for profiling, caching,
connection pooling, observability, and packaging exercises.
"""
from app.api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

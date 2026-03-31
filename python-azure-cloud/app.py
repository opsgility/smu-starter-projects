"""FastAPI application for Azure App Service deployment."""
from fastapi import FastAPI

app = FastAPI(title="CloudBridge API", version="0.1.0")

@app.get("/")
def root():
    return {"service": "CloudBridge API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

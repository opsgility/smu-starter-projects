"""SwiftRoute Package Tracking API - Starter Project"""
from fastapi import FastAPI

app = FastAPI(
    title="SwiftRoute Package Tracking API",
    description="Track shipments, manage customers, and monitor deliveries",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "SwiftRoute API is running", "version": "0.1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# TODO: Add shipment endpoints
# TODO: Add customer endpoints
# TODO: Add tracking event endpoints

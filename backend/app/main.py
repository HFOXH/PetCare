
from fastapi import FastAPI

app = FastAPI(
    title="PetCare API",
    description="API for pet health and vaccination management",
    version="0.1.0"
)

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "PetCare API",
        "version": "0.1.0"
    }


from fastapi import FastAPI

from app.api.v1.pets import router as pets_router

app = FastAPI(
    title="PetCare API",
    description="API for pet health and vaccination management",
    version="0.1.0"
)

app.include_router(pets_router, prefix="/api/v1")


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "PetCare API",
        "version": "0.1.0"
    }

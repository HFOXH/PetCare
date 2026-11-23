from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.pets import router as pets_router
from app.api.v1.users import router as users_router
from app.api.v1.species import router as species_router
from app.api.v1.vaccines import router as vaccines_router
from app.api.v1.pet_vaccinations import router as pet_vaccinations_router
from app.api.v1.gemini import router as gemini_router

app = FastAPI(
    title="PetCare API",
    description="API for pet health and vaccination management",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pets_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(species_router, prefix="/api/v1")
app.include_router(vaccines_router, prefix="/api/v1")
app.include_router(pet_vaccinations_router, prefix="/api/v1")
app.include_router(gemini_router, prefix="/api/v1")


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "PetCare API",
        "version": "0.1.0"
    }
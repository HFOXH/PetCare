import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.db.session import get_db
from app.models.pet import Pet
from app.models.pet_vaccination import PetVaccination
from app.models.vaccine import Vaccine
from app.schemas.gemini import (
    GeminiExtractionResponse,
    GeminiReviewRequest,
    GeminiReviewResponse,
)


def save_gemini_extraction(
    db: Session,
    pet_id: uuid.UUID,
    extraction: GeminiExtractionResponse,
) -> GeminiExtractionResponse:
    """
    Save data extracted by Gemini into the database.
    
    Searches for or creates a PetVaccination record for the pet and updates
    the fields with the extracted data.
    """
    # Check that the pet exists
    pet = db.get(Pet, pet_id)
    if pet is None:
        raise ValueError(f"Pet with ID {pet_id} not found")
    
    # Search if there's already a vaccination record for this pet
    # For simplicity, we create a new one or update the most recent
    stmt = select(PetVaccination).where(PetVaccination.pet_id == pet_id)
    existing = db.scalars(stmt).all()
    
    if existing:
        # Use the most recent
        vaccination = existing[0]
    else:
        # Create new record (we need a vaccine_id, for now we use an existing one or create a temporary reference)
        # For now, get the first available vaccine or create a reference
        from app.models.vaccine import Vaccine
        vaccine_stmt = select(Vaccine).limit(1)
        vaccine_result = db.scalars(vaccine_stmt).first()
        vaccine_id = vaccine_result.id if vaccine_result else uuid.uuid4()
        
        vaccination = PetVaccination(
            pet_id=pet_id,
            vaccine_id=vaccine_id,
        )
        db.add(vaccination)
    
    # Update fields with extracted data
    vaccination.administered_at = date.fromisoformat(extraction.administered_at)
    vaccination.veterinarian = extraction.veterinarian
    vaccination.next_due_at = (
        date.fromisoformat(extraction.next_due_at)
        if extraction.next_due_at
        else None
    )
    vaccination.batch_number = extraction.batch_number
    vaccination.notes = extraction.notes
    
    db.commit()
    db.refresh(vaccination)
    
    # Return formatted response
    return GeminiExtractionResponse(
        id=vaccination.id,
        pet_id=pet_id,
        vaccine_name="",  # Will be obtained from the vaccine relationship
        administered_at=vaccination.administered_at.isoformat()
        if vaccination.administered_at
        else "",
        veterinarian=vaccination.veterinarian,
        next_due_at=vaccination.next_due_at.isoformat()
        if vaccination.next_due_at
        else None,
        batch_number=vaccination.batch_number,
        notes=vaccination.notes,
        confidence=1.0,  # Default, would be calculated based on analysis success
    )


def update_gemini_extraction_review(
    db: Session,
    extraction_id: uuid.UUID,
    review_data: GeminiReviewRequest,
) -> GeminiReviewResponse:
    """
    Allows the user to review and correct data extracted by Gemini.
    
    Args:
        db: Database session
        extraction_id: ID of the extraction to update
        review_data: Data corrected by the user
    
    Returns:
        Response of the review operation
    """
    # Search for the extraction record
    stmt = select(PetVaccination).where(PetVaccination.id == extraction_id)
    vaccination = db.scalar(stmt)
    
    if vaccination is None:
        return GeminiReviewResponse(
            success=False,
            message="Extraction record not found",
            extraction_id=extraction_id,
        )
    
    # Update fields with data reviewed by the user
    if review_data.administered_at:
        vaccination.administered_at = date.fromisoformat(review_data.administered_at)
    
    if review_data.veterinarian is not None:
        vaccination.veterinarian = review_data.veterinarian
    
    if review_data.next_due_at is not None:
        vaccination.next_due_at = (
            date.fromisoformat(review_data.next_due_at)
            if review_data.next_due_at
            else None
        )
    
    if review_data.batch_number is not None:
        vaccination.batch_number = review_data.batch_number
    
    if review_data.notes is not None:
        vaccination.notes = review_data.notes
    
    db.commit()
    db.refresh(vaccination)
    
    return GeminiReviewResponse(
        success=True,
        message="Data updated successfully",
        extraction_id=vaccination.id,
    )


def get_pet_vaccination_history(
    db: Session,
    pet_id: uuid.UUID,
) -> list[GeminiExtractionResponse]:
    """
    Get the vaccination extraction history for a pet.
    """
    stmt = select(PetVaccination).where(PetVaccination.pet_id == pet_id)
    vaccinations = db.scalars(stmt).all()
    
    result = []
    for v in vaccinations:
        result.append(
            GeminiExtractionResponse(
                id=v.id,
                pet_id=v.pet_id,
                vaccine_name="",  # Will be obtained from the relationship
                administered_at=v.administered_at.isoformat()
                if v.administered_at
                else "",
                veterinarian=v.veterinarian,
                next_due_at=v.next_due_at.isoformat()
                if v.next_due_at
                else None,
                batch_number=v.batch_number,
                notes=v.notes,
                confidence=1.0,
            )
        )
    
    return result
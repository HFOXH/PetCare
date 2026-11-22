import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.pet_vaccination import (
    PetVaccinationCreate,
    PetVaccinationUpdate,
    PetVaccinationResponse,
)
from app.services.PetVaccinationService import (
    create_pet_vaccination,
    get_pet_vaccination,
    list_pet_vaccinations,
    update_pet_vaccination,
    delete_pet_vaccination,
    get_vaccination_history_by_pet,
    filter_vaccinations_by_pet_and_date,
)


router = APIRouter(prefix="/pet-vaccinations", tags=["Pet Vaccinations"])


@router.post(
    "/",
    response_model=PetVaccinationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new vaccination",
)
def create_pet_vaccination_endpoint(
    vaccination_data: PetVaccinationCreate,
    db: Session = Depends(get_db),
):
    """Register a new vaccination for a pet."""
    try:
        vaccination = create_pet_vaccination(
            db,
            pet_id=vaccination_data.pet_id,
            vaccine_id=vaccination_data.vaccine_id,
            administered_at=vaccination_data.administered_at,
            next_due_at=vaccination_data.next_due_at,
            veterinarian=vaccination_data.veterinarian,
            batch_number=vaccination_data.batch_number,
            notes=vaccination_data.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return vaccination


@router.get(
    "/",
    response_model=list[PetVaccinationResponse],
    summary="List all vaccinations",
)
def list_pet_vaccinations_endpoint(
    pet_id: uuid.UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List vaccinations, optionally filtered by pet_id."""
    vaccinations = list_pet_vaccinations(db, pet_id=pet_id, skip=skip, limit=limit)
    return vaccinations


@router.get(
    "/pet/{pet_id}",
    response_model=list[PetVaccinationResponse],
    summary="Get vaccination history for a pet",
)
def get_vaccination_history_by_pet_endpoint(
    pet_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get the vaccination history for a specific pet."""
    history = get_vaccination_history_by_pet(db, pet_id=pet_id, skip=skip, limit=limit)
    return history


@router.get(
    "/filter/",
    response_model=list[PetVaccinationResponse],
    summary="Filter vaccinations by pet and date range",
)
def filter_vaccinations(
    pet_id: uuid.UUID,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    """Filter vaccinations by pet ID and date range (inclusive)."""
    vaccinations = filter_vaccinations_by_pet_and_date(db, pet_id=pet_id, start_date=start_date, end_date=end_date)
    return vaccinations


@router.patch(
    "/{vaccination_id}",
    response_model=PetVaccinationResponse,
    summary="Update a vaccination record",
)
def update_pet_vaccination_endpoint(
    vaccination_id: uuid.UUID,
    vaccination_data: PetVaccinationUpdate,
    db: Session = Depends(get_db),
):
    """Update a vaccination record (administered_at, next_due_at, veterinarian, batch_number, notes)."""
    vaccination = get_pet_vaccination(db, vaccination_id=vaccination_id)
    if vaccination is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaccination record not found")
    try:
        updated = update_pet_vaccination(
            db,
            vaccination,
            administered_at=vaccination_data.administered_at,
            next_due_at=vaccination_data.next_due_at,
            veterinarian=vaccination_data.veterinarian,
            batch_number=vaccination_data.batch_number,
            notes=vaccination_data.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated


@router.delete(
    "/{vaccination_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a vaccination record",
)
def delete_pet_vaccination_endpoint(
    vaccination_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Delete a vaccination record."""
    vaccination = get_pet_vaccination(db, vaccination_id=vaccination_id)
    if vaccination is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaccination record not found")
    delete_pet_vaccination(db, vaccination)
"""Pet endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.services import pet_service


router = APIRouter(prefix="/pets", tags=["Pets"])


@router.post(
    "/",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_pet(
    pet_data: PetCreate,
    db: Session = Depends(get_db),
):
    """Create a new pet."""
    return pet_service.create_pet(db, pet_data)


@router.get(
    "/",
    response_model=list[PetResponse],
)
def list_pets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all pets."""
    return pet_service.get_pets(db, skip, limit)


@router.get(
    "/{pet_id}",
    response_model=PetResponse,
)
def get_pet(
    pet_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Get a pet by ID."""
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@router.patch(
    "/{pet_id}",
    response_model=PetResponse,
)
def update_pet(
    pet_id: uuid.UUID,
    pet_data: PetUpdate,
    db: Session = Depends(get_db),
):
    """Update a pet."""
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet_service.update_pet(db, pet, pet_data)


@router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_pet(
    pet_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Delete a pet."""
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    pet_service.delete_pet(db, pet)
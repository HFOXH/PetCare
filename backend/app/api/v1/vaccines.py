import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.vaccine import VaccineCreate, VaccineUpdate, VaccineResponse
from app.services.VaccineService import create_vaccine, get_vaccine, list_vaccines, update_vaccine, delete_vaccine


router = APIRouter(prefix="/vaccines", tags=["Vaccines"])


@router.post(
    "/",
    response_model=VaccineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new vaccine",
)
def create_vaccine_endpoint(
    vaccine_data: VaccineCreate,
    db: Session = Depends(get_db),
):
    """Create a new vaccine."""
    try:
        vaccine = create_vaccine(
            db,
            name=vaccine_data.name,
            description=vaccine_data.description,
            species_id=vaccine_data.species_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return vaccine


@router.get(
    "/",
    response_model=list[VaccineResponse],
    summary="List all vaccines",
)
def list_vaccines_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all vaccines."""
    vaccines = list_vaccines(db, skip=skip, limit=limit)
    return vaccines


@router.get(
    "/{vaccine_id}",
    response_model=VaccineResponse,
    summary="Get vaccine by ID",
)
def get_vaccine_endpoint(
    vaccine_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Get a vaccine by its ID."""
    vaccine = get_vaccine(db, vaccine_id=vaccine_id)
    if vaccine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaccine not found")
    return vaccine


@router.patch(
    "/{vaccine_id}",
    response_model=VaccineResponse,
    summary="Update vaccine",
)
def update_vaccine_endpoint(
    vaccine_id: uuid.UUID,
    vaccine_data: VaccineUpdate,
    db: Session = Depends(get_db),
):
    """Update a vaccine's name and/or description."""
    vaccine = get_vaccine(db, vaccine_id=vaccine_id)
    if vaccine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaccine not found")
    try:
        updated = update_vaccine(
            db, vaccine, name=vaccine_data.name, description=vaccine_data.description
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated


@router.delete(
    "/{vaccine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete vaccine",
)
def delete_vaccine_endpoint(
    vaccine_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Delete a vaccine."""
    vaccine = get_vaccine(db, vaccine_id=vaccine_id)
    if vaccine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaccine not found")
    delete_vaccine(db, vaccine)
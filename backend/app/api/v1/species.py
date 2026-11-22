import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.species import SpeciesCreate, SpeciesUpdate, SpeciesResponse
from app.services.SpeciesService import create_species, get_species, list_species, update_species, delete_species


router = APIRouter(prefix="/species", tags=["Species"])


@router.post(
    "/",
    response_model=SpeciesResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new species",
)
def create_species_endpoint(
    species_data: SpeciesCreate,
    db: Session = Depends(get_db),
):
    """Create a new species."""
    try:
        species = create_species(db, name=species_data.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return species


@router.get(
    "/",
    response_model=list[SpeciesResponse],
    summary="List all species",
)
def list_species_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all species."""
    species = list_species(db, skip=skip, limit=limit)
    return species


@router.get(
    "/{species_id}",
    response_model=SpeciesResponse,
    summary="Get species by ID",
)
def get_species_endpoint(
    species_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Get a species by its ID."""
    species = get_species(db, species_id=species_id)
    if species is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Species not found")
    return species


@router.patch(
    "/{species_id}",
    response_model=SpeciesResponse,
    summary="Update species",
)
def update_species_endpoint(
    species_id: uuid.UUID,
    species_data: SpeciesUpdate,
    db: Session = Depends(get_db),
):
    """Update a species name."""
    species = get_species(db, species_id=species_id)
    if species is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Species not found")
    try:
        updated = update_species(db, species, name=species_data.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated


@router.delete(
    "/{species_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete species",
)
def delete_species_endpoint(
    species_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Delete a species."""
    species = get_species(db, species_id=species_id)
    if species is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Species not found")
    delete_species(db, species)
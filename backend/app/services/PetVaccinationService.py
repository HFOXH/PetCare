import uuid
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.pet import Pet
from app.models.vaccine import Vaccine
from app.models.pet_vaccination import PetVaccination
from app.schemas.pet_vaccination import (
    PetVaccinationCreate,
    PetVaccinationUpdate,
    PetVaccinationResponse,
)


def create_pet_vaccination(
    db: Session,
    pet_id: uuid.UUID,
    vaccine_id: uuid.UUID,
    administered_at: date,
    next_due_at: date | None,
    veterinarian: str | None,
    batch_number: str | None,
    notes: str | None,
) -> PetVaccination:
    """Create a new pet vaccination record."""
    # Verify pet exists
    pet = db.get(Pet, pet_id)
    if pet is None:
        raise ValueError("Pet not found")
    # Verify vaccine exists
    vaccine = db.get(Vaccine, vaccine_id)
    if vaccine is None:
        raise ValueError("Vaccine not found")
    vaccination = PetVaccination(
        pet_id=pet_id,
        vaccine_id=vaccine_id,
        administered_at=administered_at,
        next_due_at=next_due_at,
        veterinarian=veterinarian,
        batch_number=batch_number,
        notes=notes,
    )
    db.add(vaccination)
    db.commit()
    db.refresh(vaccination)
    return vaccination


def get_pet_vaccination(db: Session, vaccination_id: uuid.UUID) -> PetVaccination | None:
    """Get a vaccination record by ID."""
    return db.get(PetVaccination, vaccination_id)


def list_pet_vaccinations(
    db: Session,
    pet_id: uuid.UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[PetVaccination]:
    """List vaccination records, optionally filtered by pet_id."""
    statement = select(PetVaccination)
    if pet_id is not None:
        statement = statement.where(PetVaccination.pet_id == pet_id)
    statement = statement.offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def update_pet_vaccination(
    db: Session,
    vaccination: PetVaccination,
    administered_at: date | None = None,
    next_due_at: date | None = None,
    veterinarian: str | None = None,
    batch_number: str | None = None,
    notes: str | None = None,
) -> PetVaccination:
    """Update a vaccination record."""
    if administered_at is not None:
        vaccination.administered_at = administered_at
    if next_due_at is not None:
        vaccination.next_due_at = next_due_at
    if veterinarian is not None:
        vaccination.veterinarian = veterinarian
    if batch_number is not None:
        vaccination.batch_number = batch_number
    if notes is not None:
        vaccination.notes = notes
    db.commit()
    db.refresh(vaccination)
    return vaccination


def delete_pet_vaccination(db: Session, vaccination: PetVaccination) -> None:
    """Delete a vaccination record."""
    db.delete(vaccination)
    db.commit()


def get_vaccination_history_by_pet(
    db: Session,
    pet_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[PetVaccinationResponse]:
    """Get vaccination history for a specific pet, with joined vaccine and pet names."""
    from sqlalchemy.orm import joinedload

    statement = (
        select(PetVaccination)
        .options(joinedload(PetVaccination.pet), joinedload(PetVaccination.vaccine))
        .where(PetVaccination.pet_id == pet_id)
        .offset(skip)
        .limit(limit)
    )
    vaccinations = list(db.scalars(statement).all())
    # Build response with extra info
    result = []
    for v in vaccinations:
        result.append(
            PetVaccinationResponse(
                id=v.id,
                pet_id=v.pet_id,
                vaccine_id=v.vaccine_id,
                administered_at=v.administered_at,
                next_due_at=v.next_due_at,
                veterinarian=v.veterinarian,
                batch_number=v.batch_number,
                notes=v.notes,
                pet_name=v.pet.name if v.pet else None,
                vaccine_name=v.vaccine.name if v.vaccine else None,
                created_at=v.created_at,
                updated_at=v.updated_at,
            )
        )
    return result


def filter_vaccinations_by_pet_and_date(
    db: Session,
    pet_id: uuid.UUID,
    start_date: date,
    end_date: date,
) -> list[PetVaccinationResponse]:
    """Filter vaccinations by pet and date range."""
    from sqlalchemy import between

    statement = (
        select(PetVaccination)
        .options(joinedload(PetVaccination.pet), joinedload(PetVaccination.vaccine))
        .where(
            PetVaccination.pet_id == pet_id,
            PetVaccination.administered_at.between(start_date, end_date),
        )
        .offset(0)
        .limit(100)
    )
    vaccinations = list(db.scalars(statement).all())
    result = []
    for v in vaccinations:
        result.append(
            PetVaccinationResponse(
                id=v.id,
                pet_id=v.pet_id,
                vaccine_id=v.vaccine_id,
                administered_at=v.administered_at,
                next_due_at=v.next_due_at,
                veterinarian=v.veterinarian,
                batch_number=v.batch_number,
                notes=v.notes,
                pet_name=v.pet.name if v.pet else None,
                vaccine_name=v.vaccine.name if v.vaccine else None,
                created_at=v.created_at,
                updated_at=v.updated_at,
            )
        )
    return result

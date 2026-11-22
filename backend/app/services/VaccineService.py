import uuid
from sqlalchemy import select

from app.db.session import get_db
from app.models.vaccine import Vaccine
from app.schemas.vaccine import VaccineCreate, VaccineUpdate, VaccineResponse


def create_vaccine(db, name: str, description: str | None, species_id: uuid.UUID) -> Vaccine:
    """Create a new vaccine entry."""
    vaccine = Vaccine(
        name=name,
        description=description,
        species_id=species_id,
    )
    db.add(vaccine)
    db.commit()
    db.refresh(vaccine)
    return vaccine


def get_vaccine(db, vaccine_id: uuid.UUID) -> Vaccine | None:
    """Get a vaccine by ID."""
    return db.get(Vaccine, vaccine_id)


def list_vaccines(db, skip: int = 0, limit: int = 100) -> list[Vaccine]:
    """List all vaccines with pagination."""
    stmt = select(Vaccine).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_vaccine(db, vaccine: Vaccine, name: str | None = None, description: str | None = None) -> Vaccine:
    """Update a vaccine's name and/or description."""
    if name is not None:
        vaccine.name = name
    if description is not None:
        vaccine.description = description
    db.commit()
    db.refresh(vaccine)
    return vaccine


def delete_vaccine(db, vaccine: Vaccine) -> None:
    """Delete a vaccine."""
    db.delete(vaccine)
    db.commit()
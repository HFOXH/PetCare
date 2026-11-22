import uuid
import uuid
from sqlalchemy import select

from app.db.session import get_db
from app.models.species import Species
from app.schemas.species import SpeciesCreate, SpeciesUpdate, SpeciesResponse


def create_species(db, name: str) -> Species:
    """Create a new species entry."""
    stmt = select(Species).where(Species.name == name)
    existing = db.scalar(stmt)
    if existing:
        raise ValueError("Species already exists")
    species = Species(name=name)
    db.add(species)
    db.commit()
    db.refresh(species)
    return species


def get_species(db, species_id: uuid.UUID) -> Species | None:
    """Get a species by ID."""
    return db.get(Species, species_id)


def list_species(db, skip: int = 0, limit: int = 100) -> list[Species]:
    """List all species with pagination."""
    stmt = select(Species).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_species(db, species: Species, name: str | None = None) -> Species:
    """Update a species name."""
    if name is not None:
        species.name = name
    db.commit()
    db.refresh(species)
    return species


def delete_species(db, species: Species) -> None:
    """Delete a species."""
    db.delete(species)
    db.commit()
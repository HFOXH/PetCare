import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetUpdate


def create_pet(db: Session, pet_data: PetCreate) -> Pet:
    pet = Pet(**pet_data.model_dump())

    db.add(pet)
    db.commit()
    db.refresh(pet)

    return pet


def get_pet(db: Session, pet_id: uuid.UUID) -> Pet | None:
    return db.get(Pet, pet_id)


def get_pets(db: Session, skip: int = 0, limit: int = 100) -> list[Pet]:
    statement = select(Pet).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def update_pet(
    db: Session,
    pet: Pet,
    pet_data: PetUpdate
) -> Pet:
    update_data = pet_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(pet, field, value)

    db.commit()
    db.refresh(pet)

    return pet


def delete_pet(db: Session, pet: Pet) -> None:
    db.delete(pet)
    db.commit()

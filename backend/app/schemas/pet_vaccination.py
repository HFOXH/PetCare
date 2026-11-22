import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class PetVaccinationCreate(BaseModel):
    pet_id: uuid.UUID
    vaccine_id: uuid.UUID
    administered_at: date = Field(default_factory=date.today)
    next_due_at: date | None = None
    veterinarian: str | None = None
    batch_number: str | None = None
    notes: str | None = None


class PetVaccinationUpdate(BaseModel):
    administered_at: date | None = None
    next_due_at: date | None = None
    veterinarian: str | None = None
    batch_number: str | None = None
    notes: str | None = None


class PetVaccinationResponse(BaseModel):
    id: uuid.UUID
    pet_id: uuid.UUID
    vaccine_id: uuid.UUID
    administered_at: date
    next_due_at: date | None
    veterinarian: str | None
    batch_number: str | None
    notes: str | None
    pet_name: str | None = None
    vaccine_name: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
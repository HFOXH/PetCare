import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    breed: str | None = None
    sex: str | None = None
    date_of_birth: date | None = None
    weight: float | None = Field(default=None, gt=0)
    photo_url: str | None = None
    owner_id: uuid.UUID
    species_id: uuid.UUID


class PetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    breed: str | None = None
    sex: str | None = None
    date_of_birth: date | None = None
    weight: float | None = Field(default=None, gt=0)
    photo_url: str | None = None


class PetResponse(BaseModel):
    id: uuid.UUID
    name: str
    breed: str | None
    sex: str | None
    date_of_birth: date | None
    weight: float | None
    photo_url: str | None
    owner_id: uuid.UUID
    species_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

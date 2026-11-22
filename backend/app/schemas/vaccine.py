import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class VaccineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    species_id: uuid.UUID


class VaccineUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None


class VaccineResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    species_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
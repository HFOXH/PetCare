import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, validator


class SpeciesCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, unique=True)

    @validator("name")
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError("Species name cannot be empty")
        return v.strip()


class SpeciesUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)


class SpeciesResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
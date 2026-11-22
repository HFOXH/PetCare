import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, validator


class UserCreate(BaseModel):
    email: str = Field(min_length=1, max_length=255)
    full_name: str = Field(min_length=1, max_length=150)

    @validator("email")
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("Email must contain @")
        return v


class UserLogin(BaseModel):
    email: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str | None = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
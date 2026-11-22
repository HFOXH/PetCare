import uuid
from datetime import date
from pydantic import BaseModel, Field


class GeminiUploadRequest(BaseModel):
    """Schema to upload a veterinary vaccination card image."""
    pet_id: uuid.UUID = Field(..., description="Pet ID")
    image_base64: str = Field(
        ..., description="Image in base64"
    )
    mime_type: str = Field(
        "image/jpeg", description="MIME type of the image"
    )


class GeminiExtractionResponse(BaseModel):
    """API response with Gemini extraction data."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    pet_id: uuid.UUID
    vaccine_name: str = Field(..., description="Vaccine name")
    administered_at: str = Field(..., description="Administration date in YYYY-MM-DD")
    veterinarian: str | None = Field(None, description="Veterinarian")
    next_due_at: str | None = Field(None, description="Next recommended date")
    batch_number: str | None = Field(None, description="Lot number")
    notes: str | None = Field(None, description="Additional notes")
    confidence: float = Field(
        ..., description="Extraction confidence level (0-1)"
    )
    created_at: date = Field(default_factory=date.today)

    model_config = {"from_attributes": True}


class GeminiReviewRequest(BaseModel):
    """Schema to review and correct data extracted by Gemini."""
    extraction_id: uuid.UUID = Field(
        ..., description="ID of the extraction to review"
    )
    vaccine_name: str = Field(
        ..., description="Vaccine name (corrected)"
    )
    administered_at: str = Field(
        ..., description="Corrected administration date in YYYY-MM-DD"
    )
    veterinarian: str | None = Field(
        None, description="Corrected veterinarian (optional)"
    )
    next_due_at: str | None = Field(
        None, description="Corrected next recommended date (optional)"
    )
    batch_number: str | None = Field(
        None, description="Corrected lot number (optional)"
    )
    notes: str | None = Field(
        None, description="Corrected additional notes (optional)"
    )


class GeminiReviewResponse(BaseModel):
    """Response after reviewing the data."""
    success: bool
    message: str
    extraction_id: uuid.UUID
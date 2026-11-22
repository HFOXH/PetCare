import uuid
from datetime import date
from pydantic import BaseModel, Field


class GeminiUploadRequest(BaseModel):
    """Solicitud para subir una imagen de carnet veterinario."""
    pet_id: uuid.UUID = Field(..., description="ID de la mascota")
    image_base64: str = Field(
        ..., description="Imagen en base64"
    )
    mime_type: str = Field(
        "image/jpeg", description="Tipo MIME de la imagen"
    )


class GeminiExtractionResponse(BaseModel):
    """Respuesta del análisis de Gemini."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    pet_id: uuid.UUID
    vaccine_name: str = Field(..., description="Nombre de la vacuna")
    administered_at: str = Field(..., description="Fecha de aplicación (YYYY-MM-DD)")
    veterinarian: str | None = Field(None, description="Veterinario")
    next_due_at: str | None = Field(None, description="Próxima fecha recomendada")
    batch_number: str | None = Field(None, description="Número de lote")
    notes: str | None = Field(None, description="Notas adicionales")
    confidence: float = Field(
        ..., description="Nivel de confianza de la extracción (0-1)"
    )
    created_at: date = Field(default_factory=date.today)

    model_config = {"from_attributes": True}


class GeminiReviewRequest(BaseModel):
    """Solicitud para revisar y corregir datos extraídos por Gemini."""
    extraction_id: uuid.UUID = Field(
        ..., description="ID de la extracción a revisar"
    )
    vaccine_name: str = Field(
        ..., description="Nombre de la vacuna (corregido)"
    )
    administered_at: str = Field(
        ..., description="Fecha de aplicación corregida (YYYY-MM-DD)"
    )
    veterinarian: str | None = Field(
        None, description="Veterinario corregido (opcional)"
    )
    next_due_at: str | None = Field(
        None, description="Próxima fecha recomendada corregida (opcional)"
    )
    batch_number: str | None = Field(
        None, description="Número de lote corregido (opcional)"
    )
    notes: str | None = Field(
        None, description="Notas corregidas (opcional)"
    )


class GeminiReviewResponse(BaseModel):
    """Respuesta después de revisar los datos."""
    success: bool
    message: str
    extraction_id: uuid.UUID
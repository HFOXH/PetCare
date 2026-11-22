import os
import base64
import json
from typing import Optional, Dict, Any

import google.genai as genai
from pydantic import BaseModel, Field


# Configuración de la API de Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


class GeminiExtraction(BaseModel):
    """Modelo de datos estructurados extraídos por Gemini."""
    vaccine_name: str = Field(
        ..., description="Nombre de la vacuna administrada"
    )
    administered_at: str = Field(
        ..., description="Fecha de aplicación (formato YYYY-MM-DD)"
    )
    veterinarian: Optional[str] = Field(
        None, description="Nombre del veterinario que administró la vacuna"
    )
    next_due_at: Optional[str] = Field(
        None, description="Próxima fecha recomendada por el veterinario (formato YYYY-MM-DD)"
    )
    batch_number: Optional[str] = Field(
        None, description="Número de lote de la vacuna (opcional)"
    )
    notes: Optional[str] = Field(
        None, description="Notas adicionales de la tarjeta de vacunación (opcional)"
    )

    model_config = {"extra": "allow"}


class GeminiResponse(BaseModel):
    """Respuesta de la API de Gemini con datos extraídos y metadatos."""
    extraction: GeminiExtraction
    success: bool = True
    raw_response: Optional[str] = None
    error: Optional[str] = None


def encode_image_to_base64(image_path: str) -> str:
    """Convierte una imagen a string base64 para enviar a Gemini."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_vaccination_data_from_image(
    image_base64: str,
    mime_type: str = "image/jpeg",
) -> GeminiExtraction:
    """
    Envía una imagen de carnet veterinario a Gemini y extrae los datos estructurados.
    
    Args:
        image_base64: Imagen en base64
        mime_type: Tipo MIME de la imagen
    
    Returns:
        Datos extraídos estructurados
    """
    # Configurar modelo Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = """
    Analiza esta imagen de una tarjeta de vacunación veterinaria para mascotas.
    Extrae la siguiente información y devuélvela en formato JSON estructurado:
    
    1. vaccine_name: Nombre de la vacuna administrada (obligatorio)
    2. administered_at: Fecha de aplicación en formato YYYY-MM-DD (obligatorio)
    3. veterinarian: Nombre del veterinario que administró la vacuna (opcional, puede no estar)
    4. next_due_at: Próxima fecha recomendada por el veterinario en formato YYYY-MM-DD (opcional, puede no estar)
    5. batch_number: Número de lote de la vacuna (opcional, puede no estar)
    6. notes: Cualquier otra nota o información adicional de la tarjeta (opcional)
    
    Devuelve SOLO un objeto JSON válido con estos campos. Si algún campo no se encuentra en la imagen, 
    usa un string vacío para los obligatorios y null para los opcionales.
    
    Ejemplo de salida esperada:
    {
      "vaccine_name": "Rabia",
      "administered_at": "2024-03-15",
      "veterinarian": "Dr. Juan Pérez",
      "next_due_at": "2025-03-15",
      "batch_number": "LOT-12345",
      "notes": "Primera dosis"
    }
    """

    try:
        response = model.generate_content([
            {
                "mime_type": mime_type,
                "data": base64.b64decode(image_base64),
            },
            prompt,
        ])

        # Parsear la respuesta JSON
        response_text = response.text.strip()
        
        # Intentar extraer JSON de la respuesta
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)
        else:
            # Si no hay JSON, intentar parsear el texto completo
            data = json.loads(response_text)

        # Validar y retornar usando el modelo Pydantic
        extraction = GeminiExtraction(
            vaccine_name=data.get("vaccine_name", ""),
            administered_at=data.get("administered_at", ""),
            veterinarian=data.get("veterinarian"),
            next_due_at=data.get("next_due_at"),
            batch_number=data.get("batch_number"),
            notes=data.get("notes"),
        )

        return extraction

    except Exception as e:
        # En caso de error, retornar datos por defecto
        print(f"Error en Gemini API: {str(e)}")
        return GeminiExtraction(
            vaccine_name="",
            administered_at="",
            veterinarian=None,
            next_due_at=None,
            batch_number=None,
            notes=None,
        )


def validate_extraction(extraction: GeminiExtraction) -> bool:
    """
    Valida que la extracción tenga los datos mínimos requeridos.
    
    Args:
        extraction: Datos extraídos por Gemini
    
    Returns:
        True si los datos son válidos, False en caso contrario
    """
    return (
        extraction.vaccine_name
        and extraction.administered_at
    )
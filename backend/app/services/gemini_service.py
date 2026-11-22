import os
import base64
import json
from typing import Optional, Dict, Any

import google.genai as genai
from pydantic import BaseModel, Field


# Google Gemini API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


class GeminiExtraction(BaseModel):
    """Data model structured extracted by Gemini."""
    vaccine_name: str = Field(
        ..., description="Name of the vaccine administered"
    )
    administered_at: str = Field(
        ..., description="Administration date in YYYY-MM-DD format"
    )
    veterinarian: Optional[str] = Field(
        None, description="Name of the veterinarian who administered the vaccine"
    )
    next_due_at: Optional[str] = Field(
        None, description="Next recommended date by the veterinarian in YYYY-MM-DD format"
    )
    batch_number: Optional[str] = Field(
        None, description="Vaccine lot number (optional)"
    )
    notes: Optional[str] = Field(
        None, description="Additional notes from the vaccination card (optional)"
    )

    model_config = {"extra": "allow"}


class GeminiResponse(BaseModel):
    """API response with extracted data and metadata."""
    extraction: GeminiExtraction
    success: bool = True
    raw_response: Optional[str] = None
    error: Optional[str] = None


def encode_image_to_base64(image_path: str) -> str:
    """Convert an image to base64 string to send to Gemini."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_vaccination_data_from_image(
    image_base64: str,
    mime_type: str = "image/jpeg",
) -> GeminiExtraction:
    """
    Send a veterinary vaccination card image to Gemini and extract structured data.

    Args:
        image_base64: Image in base64
        mime_type: MIME type of the image

    Returns:
        Structured extracted data
    """
    # Configure Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = """
    Analyze this veterinary vaccination card for pets to extract the following information
    and return it in structured JSON format:
    
    1. vaccine_name: Name of the vaccine administered (required)
    2. administered_at: Administration date in YYYY-MM-DD format (required)
    3. veterinarian: Name of the veterinarian who administered the vaccine (optional, may not be present)
    4. next_due_at: Next recommended date by the veterinarian in YYYY-MM-DD format (optional, may not be present)
    5. batch_number: Vaccine lot number (optional, may not be present)
    6. notes: Any other note or additional information from the card (optional)
    
    Return ONLY a valid JSON object with these fields. If any field is not found in the image,
    use an empty string for required fields and null for optional fields.
    
    Expected output example:
    {
      "vaccine_name": "Rabies",
      "administered_at": "2024-03-15",
      "veterinarian": "Dr. Juan Perez",
      "next_due_at": "2025-03-15",
      "batch_number": "LOT-12345",
      "notes": "First dose"
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

        # Parse the JSON response
        response_text = response.text.strip()
        
        # Try to extract JSON from the response
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)
        else:
            # If there's no JSON, try to parse the full text
            data = json.loads(response_text)

        # Validate and return using the Pydantic model
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
        # In case of error, return default data
        print(f"Error in Gemini API: {str(e)}")
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
    Validate that the extraction has the required minimum data.

    Args:
        extraction: Data extracted by Gemini

    Returns:
        True if the data is valid, False otherwise
    """
    return (
        extraction.vaccine_name
        and extraction.administered_at
    )
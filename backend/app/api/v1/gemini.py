import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gemini_service import (
    encode_image_to_base64,
    extract_vaccination_data_from_image,
    validate_extraction,
)
from app.services.gemini_db_service import (
    save_gemini_extraction,
    update_gemini_extraction_review,
    get_pet_vaccination_history,
)
from app.schemas.gemini import (
    GeminiUploadRequest,
    GeminiExtractionResponse,
    GeminiReviewRequest,
    GeminiReviewResponse,
)


router = APIRouter(prefix="/gemini", tags=["Gemini Integration"])


@router.post(
    "/upload",
    response_model=GeminiExtractionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload veterinary vaccination card for analysis",
)
def upload_pet_card(
    request: GeminiUploadRequest,
    db: Session = Depends(get_db),
):
    """
    Upload a pet vaccination card image and
    send to Gemini to extract vaccine data.
    """
    # Validate that the base64 image is not empty
    if not request.image_base64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image cannot be empty",
        )
    
    # Send to Gemini to extract data
    extraction = extract_vaccination_data_from_image(
        image_base64=request.image_base64,
        mime_type=request.mime_type,
    )
    
    # Validate that we have minimum data
    if not validate_extraction(extraction):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Minimum vaccine data could not be extracted "
                   "(name and date are required). "
                   "Please check the image or try again.",
        )
    
    # Create response object to save in DB
    extraction_response = GeminiExtractionResponse(
        id=uuid.uuid4(),
        pet_id=request.pet_id,
        vaccine_name=extraction.vaccine_name,
        administered_at=extraction.administered_at,
        veterinarian=extraction.veterinarian,
        next_due_at=extraction.next_due_at,
        batch_number=extraction.batch_number,
        notes=extraction.notes,
        confidence=0.9,  # Default value, could be calculated based on success
    )
    
    # Save to database
    saved = save_gemini_extraction(db, request.pet_id, extraction_response)
    
    return saved


@router.post(
    "/review",
    response_model=GeminiReviewResponse,
    summary="Review and correct data extracted by Gemini",
)
def review_extraction(
    request: GeminiReviewRequest,
    db: Session = Depends(get_db),
):
    """
    Allows the user to review and correct data extracted by Gemini.
    Confirmed data is saved to the database.
    """
    result = update_gemini_extraction_review(db, request.extraction_id, request)
    
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.message,
        )
    
    return result


@router.get(
    "/history/{pet_id}",
    response_model=list[GeminiExtractionResponse],
    summary="Get extraction history for a pet",
)
def get_history(
    pet_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Get the vaccination extraction history for a pet."""
    history = get_pet_vaccination_history(db, pet_id)
    return history
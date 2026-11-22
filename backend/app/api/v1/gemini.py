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
    summary="Subir imagen de carnet veterinario para análisis",
)
def upload_pet_card(
    request: GeminiUploadRequest,
    db: Session = Depends(get_db),
):
    """
    Sube una imagen de la tarjeta de vacunación de una mascota y
    envía a Gemini para extraer los datos de la vacuna.
    """
    # Validar que la imagen base64 no esté vacía
    if not request.image_base64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen no puede estar vacía",
        )
    
    # Enviar a Gemini para extraer datos
    extraction = extract_vaccination_data_from_image(
        image_base64=request.image_base64,
        mime_type=request.mime_type,
    )
    
    # Validar que tengamos los datos mínimos
    if not validate_extraction(extraction):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No se pudieron extraer los datos mínimos de la vacuna "
                   "(nombre y fecha son obligatorios). "
                   "Por favor, verifique la imagen o intente de nuevo.",
        )
    
    # Crear objeto de respuesta para guardar en BD
    extraction_response = GeminiExtractionResponse(
        id=uuid.uuid4(),
        pet_id=request.pet_id,
        vaccine_name=extraction.vaccine_name,
        administered_at=extraction.administered_at,
        veterinarian=extraction.veterinarian,
        next_due_at=extraction.next_due_at,
        batch_number=extraction.batch_number,
        notes=extraction.notes,
        confidence=0.9,  # Valor por defecto, se podría calcular basándose en el éxito
    )
    
    # Guardar en la base de datos
    saved = save_gemini_extraction(db, request.pet_id, extraction_response)
    
    return saved


@router.post(
    "/review",
    response_model=GeminiReviewResponse,
    summary="Revisar y corregir datos extraídos por Gemini",
)
def review_extraction(
    request: GeminiReviewRequest,
    db: Session = Depends(get_db),
):
    """
    Permite al usuario revisar y corregir los datos extraídos por Gemini.
    Los datos confirmados se guardan en la base de datos.
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
    summary="Obtener historial de extracciones para una mascota",
)
def get_history(
    pet_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Obtiene el historial de extracciones de vacunas para una mascota."""
    history = get_pet_vaccination_history(db, pet_id)
    return history
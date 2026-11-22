import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.db.session import get_db
from app.models.pet import Pet
from app.models.pet_vaccination import PetVaccination
from app.models.vaccine import Vaccine
from app.schemas.gemini import (
    GeminiExtractionResponse,
    GeminiReviewRequest,
    GeminiReviewResponse,
)


def save_gemini_extraction(
    db: Session,
    pet_id: uuid.UUID,
    extraction: GeminiExtractionResponse,
) -> GeminiExtractionResponse:
    """
    Guarda los datos extraídos por Gemini en la base de datos.
    
    Busca o crea un registro de PetVaccination para la mascota y actualiza
    los campos con los datos extraídos.
    """
    # Verificar que la mascota existe
    pet = db.get(Pet, pet_id)
    if pet is None:
        raise ValueError(f"Mascota con ID {pet_id} no encontrada")
    
    # Buscar si ya existe un registro de vacunación para esta mascota
    # Por simplicidad, creamos uno nuevo o actualizamos el más reciente
    stmt = select(PetVaccination).where(PetVaccination.pet_id == pet_id)
    existing = db.scalars(stmt).all()
    
    if existing:
        # Usar el más reciente
        vaccination = existing[0]
    else:
        # Crear nuevo registro (necesitamos un vaccine_id, por ahora usamos uno existente o creamos uno temporal)
        # Por ahora, obtemos la primera vacuna disponible o creamos una referencia
        from app.models.vaccine import Vaccine
        vaccine_stmt = select(Vaccine).limit(1)
        vaccine_result = db.scalars(vaccine_stmt).first()
        vaccine_id = vaccine_result.id if vaccine_result else uuid.uuid4()
        
        vaccination = PetVaccination(
            pet_id=pet_id,
            vaccine_id=vaccine_id,
        )
        db.add(vaccination)
    
    # Actualizar campos con los datos extraídos
    vaccination.administered_at = date.fromisoformat(extraction.administered_at)
    vaccination.veterinarian = extraction.veterinarian
    vaccination.next_due_at = (
        date.fromisoformat(extraction.next_due_at)
        if extraction.next_due_at
        else None
    )
    vaccination.batch_number = extraction.batch_number
    vaccination.notes = extraction.notes
    
    db.commit()
    db.refresh(vaccination)
    
    # Retornar respuesta formateada
    return GeminiExtractionResponse(
        id=vaccination.id,
        pet_id=pet_id,
        vaccine_name="",  # Se obtendría de la relación con vaccine
        administered_at=vaccination.administered_at.isoformat()
        if vaccination.administered_at
        else "",
        veterinarian=vaccination.veterinarian,
        next_due_at=vaccination.next_due_at.isoformat()
        if vaccination.next_due_at
        else None,
        batch_number=vaccination.batch_number,
        notes=vaccination.notes,
        confidence=1.0,  # Por defecto, se calcularía en base al éxito del análisis
    )


def update_gemini_extraction_review(
    db: Session,
    extraction_id: uuid.UUID,
    review_data: GeminiReviewRequest,
) -> GeminiReviewResponse:
    """
    Permite al usuario revisar y corregir los datos extraídos por Gemini.
    
    Args:
        db: Sesión de base de datos
        extraction_id: ID de la extracción a actualizar
        review_data: Datos corregidos por el usuario
    
    Returns:
        Respuesta de la operación de revisión
    """
    # Buscar el registro de extracción
    stmt = select(PetVaccination).where(PetVaccination.id == extraction_id)
    vaccination = db.scalar(stmt)
    
    if vaccination is None:
        return GeminiReviewResponse(
            success=False,
            message="Registro de extracción no encontrado",
            extraction_id=extraction_id,
        )
    
    # Actualizar campos con los datos revisados por el usuario
    if review_data.vaccine_name:
        # Nota: vaccine_id es una relación, aquí solo actualizaríamos el nombre
        # en un caso real, podríamos tener una tabla separada de vacunas extraídas
        pass
    
    if review_data.administered_at:
        vaccination.administered_at = date.fromisoformat(review_data.administered_at)
    
    if review_data.veterinarian is not None:
        vaccination.veterinarian = review_data.veterinarian
    
    if review_data.next_due_at is not None:
        vaccination.next_due_at = (
            date.fromisoformat(review_data.next_due_at)
            if review_data.next_due_at
            else None
        )
    
    if review_data.batch_number is not None:
        vaccination.batch_number = review_data.batch_number
    
    if review_data.notes is not None:
        vaccination.notes = review_data.notes
    
    db.commit()
    db.refresh(vaccination)
    
    return GeminiReviewResponse(
        success=True,
        message="Datos actualizados exitosamente",
        extraction_id=vaccination.id,
    )


def get_pet_vaccination_history(
    db: Session,
    pet_id: uuid.UUID,
) -> list[GeminiExtractionResponse]:
    """
    Obtiene el historial de extracciones de vacunas para una mascota.
    """
    stmt = select(PetVaccination).where(PetVaccination.pet_id == pet_id)
    vaccinations = db.scalars(stmt).all()
    
    result = []
    for v in vaccinations:
        result.append(
            GeminiExtractionResponse(
                id=v.id,
                pet_id=v.pet_id,
                vaccine_name="",  # Se obtendría de la relación
                administered_at=v.administered_at.isoformat()
                if v.administered_at
                else "",
                veterinarian=v.veterinarian,
                next_due_at=v.next_due_at.isoformat()
                if v.next_due_at
                else None,
                batch_number=v.batch_number,
                notes=v.notes,
                confidence=1.0,
            )
        )
    
    return result
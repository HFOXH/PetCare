export interface Vaccine {
  id: string;
  name: string;
  description?: string;
  species_id: string;
  created_at: string;
  updated_at: string;
}

export interface VaccineCreate {
  name: string;
  description?: string;
  species_id: string;
}

export interface VaccineUpdate {
  name?: string;
  description?: string;
}

export interface Species {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface SpeciesCreate {
  name: string;
}

export interface PetVaccination {
  id: string;
  pet_id: string;
  vaccine_id: string;
  administered_at: string;
  next_due_at?: string;
  veterinarian?: string;
  batch_number?: string;
  notes?: string;
  pet_name?: string;
  vaccine_name?: string;
  created_at: string;
  updated_at: string;
}

export interface PetVaccinationCreate {
  pet_id: string;
  vaccine_id: string;
  administered_at: string;
  next_due_at?: string;
  veterinarian?: string;
  batch_number?: string;
  notes?: string;
}

export interface GeminiExtraction {
  id: string;
  pet_id: string;
  vaccine_name: string;
  administered_at: string;
  veterinarian?: string;
  next_due_at?: string;
  batch_number?: string;
  notes?: string;
  confidence: number;
  created_at: string;
}

export interface GeminiUploadRequest {
  pet_id: string;
  image_base64: string;
  mime_type: string;
}

export interface GeminiReviewRequest {
  extraction_id: string;
  vaccine_name: string;
  administered_at: string;
  veterinarian?: string;
  next_due_at?: string;
  batch_number?: string;
  notes?: string;
}
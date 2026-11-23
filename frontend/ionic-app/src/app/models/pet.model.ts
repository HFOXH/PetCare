export interface Pet {
  id: string;
  name: string;
  breed?: string;
  sex?: string;
  date_of_birth?: string;
  weight?: number;
  photo_url?: string;
  owner_id: string;
  species_id: string;
  created_at: string;
  updated_at: string;
}

export interface PetCreate {
  name: string;
  breed?: string;
  sex?: string;
  date_of_birth?: string;
  weight?: number;
  photo_url?: string;
  owner_id: string;
  species_id: string;
}

export interface PetUpdate {
  name?: string;
  breed?: string;
  sex?: string;
  date_of_birth?: string;
  weight?: number;
  photo_url?: string;
}
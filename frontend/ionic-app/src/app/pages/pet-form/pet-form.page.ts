import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonSpinner,
  IonIcon,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { save, arrowBack } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { PetCreate, PetUpdate } from '../../models/pet.model';
import { Species } from '../../models/vaccine.model';

@Component({
  selector: 'app-pet-form',
  templateUrl: 'pet-form.page.html',
  styleUrls: ['pet-form.page.scss'],
  imports: [
    CommonModule,
    FormsModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonButton,
    IonSpinner,
    IonIcon,
  ],
})
export class PetFormPage implements OnInit {
  isEdit = false;
  petId = '';
  isLoading = false;
  errorMessage = '';

  // Form fields
  name = '';
  breed = '';
  sex = '';
  dateOfBirth = '';
  weight: number | null = null;
  speciesId = '';
  speciesList: Species[] = [];

  constructor(
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute,
  ) {
    addIcons({ save, arrowBack });
  }

  ngOnInit() {
    this.loadSpecies();
    this.petId = this.route.snapshot.paramMap.get('id') || '';
    this.isEdit = !!this.petId;
    if (this.isEdit) {
      this.loadPet();
    }
  }

  loadSpecies() {
    this.api.getSpecies().subscribe({
      next: (species) => {
        this.speciesList = species;
      },
      error: (err) => {
        console.error('Failed to load species', err);
      },
    });
  }

  loadPet() {
    this.isLoading = true;
    this.api.getPet(this.petId).subscribe({
      next: (pet) => {
        this.name = pet.name;
        this.breed = pet.breed || '';
        this.sex = pet.sex || '';
        this.dateOfBirth = pet.date_of_birth || '';
        this.weight = pet.weight || null;
        this.speciesId = pet.species_id || '';
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to load pet';
      },
    });
  }

  savePet() {
    if (!this.name || !this.speciesId) {
      this.errorMessage = 'Name and species are required';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    if (this.isEdit) {
      const data: PetUpdate = {
        name: this.name,
        breed: this.breed || undefined,
        sex: this.sex || undefined,
        date_of_birth: this.dateOfBirth || undefined,
        weight: this.weight || undefined,
      };
      this.api.updatePet(this.petId, data).subscribe({
        next: () => {
          this.isLoading = false;
          this.router.navigate(['/pets']);
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = err.message || 'Failed to update pet';
        },
      });
    } else {
      const data: PetCreate = {
        name: this.name,
        breed: this.breed || undefined,
        sex: this.sex || undefined,
        date_of_birth: this.dateOfBirth || undefined,
        weight: this.weight || undefined,
        owner_id: 'placeholder', // TODO: Get from auth context
        species_id: this.speciesId,
      };
      this.api.createPet(data).subscribe({
        next: () => {
          this.isLoading = false;
          this.router.navigate(['/pets']);
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = err.message || 'Failed to create pet';
        },
      });
    }
  }

  goBack() {
    this.router.navigate(['/pets']);
  }
}

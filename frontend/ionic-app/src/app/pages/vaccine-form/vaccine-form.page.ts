import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonItem, IonLabel, IonInput, IonSelect, IonSelectOption, IonButton, IonSpinner, IonIcon } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { save, arrowBack } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { PetVaccinationCreate } from '../../models/vaccine.model';
import { Vaccine } from '../../models/vaccine.model';

@Component({
  selector: 'app-vaccine-form',
  templateUrl: 'vaccine-form.page.html',
  styleUrls: ['vaccine-form.page.scss'],
  imports: [CommonModule, FormsModule, IonHeader, IonToolbar, IonTitle, IonContent, IonItem, IonLabel, IonInput, IonSelect, IonSelectOption, IonButton, IonSpinner, IonIcon],
})
export class VaccineFormPage implements OnInit {
  petId = '';
  isLoading = false;
  errorMessage = '';

  // Form fields
  vaccineId = '';
  administeredAt = '';
  nextDueAt = '';
  veterinarian = '';
  batchNumber = '';
  notes = '';

  vaccines: Vaccine[] = [];

  constructor(private api: ApiService, private router: Router, private route: ActivatedRoute) {
    addIcons({ save, arrowBack });
  }

  ngOnInit() {
    this.petId = this.route.snapshot.paramMap.get('id') || '';
    this.loadVaccines();
  }

  loadVaccines() {
    this.api.getVaccines().subscribe({
      next: (vaccines) => {
        this.vaccines = vaccines;
      },
      error: (err) => {
        console.error('Failed to load vaccines', err);
      }
    });
  }

  saveVaccination() {
    if (!this.vaccineId || !this.administeredAt) {
      this.errorMessage = 'Vaccine and administration date are required';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const data: PetVaccinationCreate = {
      pet_id: this.petId,
      vaccine_id: this.vaccineId,
      administered_at: this.administeredAt,
      next_due_at: this.nextDueAt || undefined,
      veterinarian: this.veterinarian || undefined,
      batch_number: this.batchNumber || undefined,
      notes: this.notes || undefined,
    };

    this.api.createPetVaccination(data).subscribe({
      next: () => {
        this.isLoading = false;
        this.router.navigate(['/pets', this.petId, 'vaccinations']);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to save vaccination';
      }
    });
  }

  goBack() {
    this.router.navigate(['/pets', this.petId, 'vaccinations']);
  }
}
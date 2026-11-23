import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute } from '@angular/router';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon, IonList, IonItem, IonLabel, IonSpinner } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { create, trash, medical, camera } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { Pet } from '../../models/pet.model';

@Component({
  selector: 'app-pet-detail',
  templateUrl: 'pet-detail.page.html',
  styleUrls: ['pet-detail.page.scss'],
  imports: [CommonModule, IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon, IonList, IonItem, IonLabel, IonSpinner],
})
export class PetDetailPage implements OnInit {
  pet: Pet | null = null;
  isLoading = false;
  errorMessage = '';

  constructor(private api: ApiService, private router: Router, private route: ActivatedRoute) {
    addIcons({ create, trash, medical, camera });
  }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadPet(id);
    }
  }

  loadPet(id: string) {
    this.isLoading = true;
    this.api.getPet(id).subscribe({
      next: (pet) => {
        this.pet = pet;
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to load pet';
      }
    });
  }

  editPet() {
    if (this.pet) {
      this.router.navigate(['/pets', this.pet.id, 'edit']);
    }
  }

  deletePet() {
    if (this.pet && confirm('Are you sure you want to delete this pet?')) {
      this.api.deletePet(this.pet.id).subscribe({
        next: () => {
          this.router.navigate(['/pets']);
        },
        error: (err) => {
          this.errorMessage = err.message || 'Failed to delete pet';
        }
      });
    }
  }

  viewVaccinations() {
    if (this.pet) {
      this.router.navigate(['/pets', this.pet.id, 'vaccinations']);
    }
  }

  scanCard() {
    if (this.pet) {
      this.router.navigate(['/scan'], { queryParams: { petId: this.pet.id } });
    }
  }

  goBack() {
    this.router.navigate(['/pets']);
  }
}
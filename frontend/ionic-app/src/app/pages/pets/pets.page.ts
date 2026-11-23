import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem,
  IonLabel,
  IonAvatar,
  IonButton,
  IonIcon,
  IonFab,
  IonFabButton,
  IonSpinner,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { add, paw, arrowBack } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { Pet } from '../../models/pet.model';

@Component({
  selector: 'app-pets',
  templateUrl: 'pets.page.html',
  styleUrls: ['pets.page.scss'],
  imports: [
    CommonModule,
    FormsModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonList,
    IonItem,
    IonLabel,
    IonAvatar,
    IonButton,
    IonIcon,
    IonFab,
    IonFabButton,
    IonSpinner,
  ],
})
export class PetsPage implements OnInit {
  pets: Pet[] = [];
  isLoading = false;
  errorMessage = '';

  constructor(
    private api: ApiService,
    private router: Router,
  ) {
    addIcons({ add, paw, arrowBack });
  }

  ngOnInit() {
    this.loadPets();
  }

  loadPets() {
    this.isLoading = true;
    this.api.getPets().subscribe({
      next: (pets) => {
        this.pets = pets;
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to load pets';
      },
    });
  }

  goToNewPet() {
    this.router.navigate(['/pets/new']);
  }

  goToPetDetail(id: string) {
    this.router.navigate(['/pets', id]);
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }
}

import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel, IonButton, IonIcon, IonFab, IonFabButton, IonSpinner } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { add, arrowBack, medical } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { PetVaccination } from '../../models/vaccine.model';

@Component({
  selector: 'app-vaccination-history',
  templateUrl: 'vaccination-history.page.html',
  styleUrls: ['vaccination-history.page.scss'],
  imports: [CommonModule, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel, IonButton, IonIcon, IonFab, IonFabButton, IonSpinner],
})
export class VaccinationHistoryPage implements OnInit {
  petId = '';
  vaccinations: PetVaccination[] = [];
  isLoading = false;
  errorMessage = '';

  constructor(private api: ApiService, private router: Router, private route: ActivatedRoute) {
    addIcons({ add, arrowBack, medical });
  }

  ngOnInit() {
    this.petId = this.route.snapshot.paramMap.get('id') || '';
    if (this.petId) {
      this.loadVaccinations();
    }
  }

  loadVaccinations() {
    this.isLoading = true;
    this.api.getVaccinationHistory(this.petId).subscribe({
      next: (vaccinations) => {
        this.vaccinations = vaccinations;
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to load vaccinations';
      }
    });
  }

  goToAddVaccination() {
    this.router.navigate(['/pets', this.petId, 'vaccinations', 'new']);
  }

  goBack() {
    this.router.navigate(['/pets', this.petId]);
  }
}
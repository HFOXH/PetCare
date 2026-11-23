import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon, IonGrid, IonRow, IonCol } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { paw, camera, calendar, medical } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: 'dashboard.page.html',
  styleUrls: ['dashboard.page.scss'],
  imports: [IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon, IonGrid, IonRow, IonCol],
})
export class DashboardPage {
  constructor(private api: ApiService, private router: Router) {
    addIcons({ paw, camera, calendar, medical });
  }

  goToPets() {
    this.router.navigate(['/pets']);
  }

  goToScan() {
    this.router.navigate(['/scan']);
  }

  goToReminders() {
    this.router.navigate(['/reminders']);
  }

  logout() {
    this.api.clearToken();
    this.router.navigate(['/welcome']);
  }
}
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel, IonIcon, IonSpinner, IonButton } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { calendar, arrowBack, medical } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-reminders',
  templateUrl: 'reminders.page.html',
  styleUrls: ['reminders.page.scss'],
  imports: [CommonModule, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel, IonIcon, IonSpinner, IonButton],
})
export class RemindersPage implements OnInit {
  reminders: any[] = [];
  isLoading = false;
  errorMessage = '';

  constructor(private api: ApiService, private router: Router) {
    addIcons({ calendar, arrowBack, medical });
  }

  ngOnInit() {
    this.loadReminders();
  }

  loadReminders() {
    this.isLoading = true;
    // For now, load all vaccinations and filter those with next_due_at
    this.api.getPetVaccinations().subscribe({
      next: (vaccinations) => {
        this.reminders = vaccinations.filter((v: any) => v.next_due_at);
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to load reminders';
      }
    });
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }
}
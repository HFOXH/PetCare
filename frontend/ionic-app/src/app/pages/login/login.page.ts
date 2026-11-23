import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonItem, IonLabel, IonInput, IonButton, IonIcon, IonSpinner } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { mail, lockClosed, arrowBack } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { UserLogin } from '../../models/user.model';

@Component({
  selector: 'app-login',
  templateUrl: 'login.page.html',
  styleUrls: ['login.page.scss'],
  imports: [CommonModule, IonHeader, IonToolbar, IonTitle, IonContent, IonItem, IonLabel, IonInput, IonButton, IonIcon, IonSpinner, FormsModule],
})
export class LoginPage {
  email = '';
  password = '';
  isLoading = false;
  errorMessage = '';

  constructor(private api: ApiService, private router: Router) {
    addIcons({ mail, lockClosed, arrowBack });
  }

  async login() {
    this.isLoading = true;
    this.errorMessage = '';
    const data: UserLogin = { email: this.email, password: this.password };
    this.api.login(data).subscribe({
      next: () => {
        this.isLoading = false;
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Login failed';
      }
    });
  }

  goBack() {
    this.router.navigate(['/welcome']);
  }
}
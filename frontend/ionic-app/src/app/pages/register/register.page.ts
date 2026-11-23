import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonIcon,
  IonSpinner,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { person, mail, lockClosed, arrowBack } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { UserRegister } from '../../models/user.model';

@Component({
  selector: 'app-register',
  templateUrl: 'register.page.html',
  styleUrls: ['register.page.scss'],
  imports: [
    CommonModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonIcon,
    IonSpinner,
    FormsModule,
  ],
})
export class RegisterPage {
  fullName = '';
  email = '';
  password = '';
  isLoading = false;
  errorMessage = '';

  constructor(
    private api: ApiService,
    private router: Router,
  ) {
    addIcons({ person, mail, lockClosed, arrowBack });
  }

  async register() {
    this.isLoading = true;
    this.errorMessage = '';
    const data: UserRegister = { email: this.email, full_name: this.fullName, password: this.password };
    this.api.register(data).subscribe({
      next: () => {
        this.isLoading = false;
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Registration failed';
      },
    });
  }

  goBack() {
    this.router.navigate(['/welcome']);
  }
}

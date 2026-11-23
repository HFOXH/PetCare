import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon, IonSpinner } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { camera, image, arrowBack } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-scan',
  templateUrl: 'scan.page.html',
  styleUrls: ['scan.page.scss'],
  imports: [CommonModule, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon, IonSpinner],
})
export class ScanPage {
  petId = '';
  isLoading = false;
  errorMessage = '';
  imageBase64 = '';
  mimeType = 'image/jpeg';

  constructor(private api: ApiService, private router: Router) {
    addIcons({ camera, image, arrowBack });
    const params = new URLSearchParams(window.location.search);
    this.petId = params.get('petId') || '';
  }

  async takePhoto() {
    // In a real app, use Capacitor Camera plugin
    // For now, simulate with file input
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (event: any) => {
      const file = event.target.files[0];
      if (file) {
        this.processImage(file);
      }
    };
    input.click();
  }

  processImage(file: File) {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      this.imageBase64 = result.split(',')[1];
      this.mimeType = file.type || 'image/jpeg';
      this.uploadImage();
    };
    reader.readAsDataURL(file);
  }

  uploadImage() {
    this.isLoading = true;
    this.errorMessage = '';

    const data = {
      pet_id: this.petId,
      image_base64: this.imageBase64,
      mime_type: this.mimeType,
    };

    this.api.uploadPetCard(data).subscribe({
      next: (result) => {
        this.isLoading = false;
        this.router.navigate(['/review-extraction', result.id], { state: { extraction: result } });
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to scan card';
      }
    });
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }
}
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
  IonButton,
  IonIcon,
  IonSpinner,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { save, arrowBack } from 'ionicons/icons';
import { ApiService } from '../../services/api.service';
import { GeminiExtraction, GeminiReviewRequest } from '../../models/vaccine.model';

@Component({
  selector: 'app-review-extraction',
  templateUrl: 'review-extraction.page.html',
  styleUrls: ['review-extraction.page.scss'],
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
    IonButton,
    IonIcon,
    IonSpinner,
  ],
})
export class ReviewExtractionPage implements OnInit {
  extraction: GeminiExtraction | null = null;
  isLoading = false;
  errorMessage = '';

  // Form fields
  vaccineName = '';
  administeredAt = '';
  veterinarian = '';
  nextDueAt = '';
  batchNumber = '';
  notes = '';

  constructor(
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute,
  ) {
    addIcons({ save, arrowBack });
  }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id') || '';
    const state = (window as any).history.state;
    if (state?.extraction) {
      this.extraction = state.extraction;
      this.populateForm();
    } else if (id) {
      // Load extraction from API
      this.loadExtraction(id);
    }
  }

  loadExtraction(id: string) {
    // For now, just navigate back
    this.router.navigate(['/dashboard']);
  }

  populateForm() {
    if (this.extraction) {
      this.vaccineName = this.extraction.vaccine_name || '';
      this.administeredAt = this.extraction.administered_at || '';
      this.veterinarian = this.extraction.veterinarian || '';
      this.nextDueAt = this.extraction.next_due_at || '';
      this.batchNumber = this.extraction.batch_number || '';
      this.notes = this.extraction.notes || '';
    }
  }

  saveExtraction() {
    if (!this.vaccineName || !this.administeredAt) {
      this.errorMessage = 'Vaccine name and administration date are required';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const data: GeminiReviewRequest = {
      extraction_id: this.extraction?.id || '',
      vaccine_name: this.vaccineName,
      administered_at: this.administeredAt,
      veterinarian: this.veterinarian || undefined,
      next_due_at: this.nextDueAt || undefined,
      batch_number: this.batchNumber || undefined,
      notes: this.notes || undefined,
    };

    this.api.reviewExtraction(data).subscribe({
      next: () => {
        this.isLoading = false;
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Failed to save extraction';
      },
    });
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }
}

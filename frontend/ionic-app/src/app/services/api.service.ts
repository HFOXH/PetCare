import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl || 'http://localhost:8000/api/v1';
  private tokenSubject = new BehaviorSubject<string | null>(null);
  public token$ = this.tokenSubject.asObservable();

  constructor(private http: HttpClient) {
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.tokenSubject.next(token);
    }
  }

  private getHeaders(): HttpHeaders {
    const token = this.tokenSubject.value;
    if (token) {
      return new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      });
    }
    return new HttpHeaders({ 'Content-Type': 'application/json' });
  }

  setToken(token: string): void {
    localStorage.setItem('auth_token', token);
    this.tokenSubject.next(token);
  }

  clearToken(): void {
    localStorage.removeItem('auth_token');
    this.tokenSubject.next(null);
  }

  getToken(): string | null {
    return this.tokenSubject.value;
  }

  isAuthenticated(): boolean {
    return !!this.tokenSubject.value;
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An unknown error occurred';
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = error.error?.detail || `Error Code: ${error.status}`;
    }
    return throwError(() => new Error(errorMessage));
  }

  // Auth endpoints
  register(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/register`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  login(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/login`, data, { headers: this.getHeaders() }).pipe(
      tap((response: any) => {
        if (response?.access_token) {
          this.setToken(response.access_token);
        }
      }),
      catchError(this.handleError)
    );
  }

  // Pets
  getPets(skip = 0, limit = 100): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pets/?skip=${skip}&limit=${limit}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  getPet(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/pets/${id}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  createPet(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/pets/`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  updatePet(id: string, data: any): Observable<any> {
    return this.http.patch(`${this.apiUrl}/pets/${id}`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  deletePet(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/pets/${id}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  // Species
  getSpecies(skip = 0, limit = 100): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/species/?skip=${skip}&limit=${limit}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  getSpeciesById(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/species/${id}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  createSpecies(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/species/`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  // Vaccines
  getVaccines(skip = 0, limit = 100): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/vaccines/?skip=${skip}&limit=${limit}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  getVaccine(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/vaccines/${id}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  createVaccine(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/vaccines/`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  // Pet Vaccinations
  getPetVaccinations(petId?: string, skip = 0, limit = 100): Observable<any[]> {
    let url = `${this.apiUrl}/pet-vaccinations/?skip=${skip}&limit=${limit}`;
    if (petId) {
      url += `&pet_id=${petId}`;
    }
    return this.http.get<any[]>(url, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  getVaccinationHistory(petId: string, skip = 0, limit = 100): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pet-vaccinations/pet/${petId}?skip=${skip}&limit=${limit}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  createPetVaccination(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/pet-vaccinations/`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  updatePetVaccination(id: string, data: any): Observable<any> {
    return this.http.patch(`${this.apiUrl}/pet-vaccinations/${id}`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  deletePetVaccination(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/pet-vaccinations/${id}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  // Gemini
  uploadPetCard(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/gemini/upload`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  reviewExtraction(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/gemini/review`, data, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }

  getGeminiHistory(petId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/gemini/history/${petId}`, { headers: this.getHeaders() }).pipe(
      catchError(this.handleError)
    );
  }
}
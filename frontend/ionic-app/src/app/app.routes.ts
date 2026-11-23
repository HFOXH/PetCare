import type { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'welcome',
    loadComponent: () => import('./pages/welcome/welcome.page').then((m) => m.WelcomePage),
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.page').then((m) => m.LoginPage),
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.page').then((m) => m.RegisterPage),
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./pages/dashboard/dashboard.page').then((m) => m.DashboardPage),
  },
  {
    path: 'pets',
    loadComponent: () => import('./pages/pets/pets.page').then((m) => m.PetsPage),
  },
  {
    path: 'pets/new',
    loadComponent: () => import('./pages/pet-form/pet-form.page').then((m) => m.PetFormPage),
  },
  {
    path: 'pets/:id',
    loadComponent: () => import('./pages/pet-detail/pet-detail.page').then((m) => m.PetDetailPage),
  },
  {
    path: 'pets/:id/edit',
    loadComponent: () => import('./pages/pet-form/pet-form.page').then((m) => m.PetFormPage),
  },
  {
    path: 'pets/:id/vaccinations',
    loadComponent: () => import('./pages/vaccination-history/vaccination-history.page').then((m) => m.VaccinationHistoryPage),
  },
  {
    path: 'pets/:id/vaccinations/new',
    loadComponent: () => import('./pages/vaccine-form/vaccine-form.page').then((m) => m.VaccineFormPage),
  },
  {
    path: 'scan',
    loadComponent: () => import('./pages/scan/scan.page').then((m) => m.ScanPage),
  },
  {
    path: 'review-extraction/:id',
    loadComponent: () => import('./pages/review-extraction/review-extraction.page').then((m) => m.ReviewExtractionPage),
  },
  {
    path: 'reminders',
    loadComponent: () => import('./pages/reminders/reminders.page').then((m) => m.RemindersPage),
  },
  {
    path: '',
    redirectTo: 'welcome',
    pathMatch: 'full',
  },
];
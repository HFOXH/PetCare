import { Injectable, signal, computed } from '@angular/core';

export type ThemeMode = 'light' | 'dark';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly storageKey = 'petcare-theme';

  readonly theme = signal<ThemeMode>(this.initialTheme());
  readonly dark = computed(() => this.theme() === 'dark');

  constructor() {
    // Apply initial theme
    this.applyTheme(this.theme());
  }

  toggle(): void {
    const newMode = this.theme() === 'dark' ? 'light' : 'dark';
    this.theme.set(newMode);
    this.applyTheme(newMode);
  }

  set(mode: ThemeMode): void {
    this.theme.set(mode);
    this.applyTheme(mode);
  }

  private applyTheme(mode: ThemeMode): void {
    const isDark = mode === 'dark';
    const root = document.documentElement;
    const body = document.body;

    // Toggle dark palette class on both html and body
    root.classList.toggle('ion-palette-dark', isDark);
    body.classList.toggle('ion-palette-dark', isDark);

    // Set color-scheme for native elements
    root.style.colorScheme = isDark ? 'dark' : 'light';

    // Also toggle on ion-app if it exists
    const ionApp = document.querySelector('ion-app');
    if (ionApp) {
      ionApp.classList.toggle('ion-palette-dark', isDark);
    }

    try {
      localStorage.setItem(this.storageKey, mode);
    } catch {
      /* ignore */
    }
  }

  private initialTheme(): ThemeMode {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored === 'light' || stored === 'dark') return stored;
    } catch {
      /* ignore */
    }
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light';
  }
}
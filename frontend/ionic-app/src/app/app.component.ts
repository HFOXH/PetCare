import { Component } from '@angular/core';
import { IonApp, IonIcon, IonRouterOutlet } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { moon, sunny } from 'ionicons/icons';

import { ThemeService } from './services/theme.service';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  imports: [IonApp, IonRouterOutlet, IonIcon],
})
export class AppComponent {
  constructor(public theme: ThemeService) {
    addIcons({ sunny, moon });
  }
}

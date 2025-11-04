import { Routes } from '@angular/router';
import { MapComponent } from './components/map/map.component';
import { LoginComponent } from './pages/login/login.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { MapPageComponent } from './pages/map/map-page.component';

export const routes: Routes = [
   { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'map', component: MapPageComponent },
  { path: '**', redirectTo: 'login' }
];

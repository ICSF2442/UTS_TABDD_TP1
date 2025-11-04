import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  email = '';
  password = '';

  constructor(private router: Router) {}

  login() {
    // TODO: connect to FastAPI login endpoint
    console.log('Logging in:', this.email);
    this.router.navigate(['/map']);
  }
}

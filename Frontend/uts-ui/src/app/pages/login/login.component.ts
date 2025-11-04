import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  imports: [FormsModule],
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  email = '';
  password = '';
  keepSession = false;

  constructor(private router: Router) {}

  login() {
    // TODO: Connect to FastAPI /auth endpoint
    console.log('Login:', this.email, this.password, 'Keep session:', this.keepSession);

    // Mock login for now
    if (this.email && this.password) {
      this.router.navigate(['/map']);
    } else {
      alert('Please enter valid credentials.');
    }
  }
}

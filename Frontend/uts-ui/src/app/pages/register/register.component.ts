import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'register',
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  loading = false;

  onSubmit() {
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
      alert('Account created successfully!');
    }, 2000);
  }
}
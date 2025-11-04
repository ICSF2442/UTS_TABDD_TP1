import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'search-bar',
  templateUrl: './search-bar.component.html',
  imports: [FormsModule],
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent {
  query: string = '';
  focused = false;

  onFocus() {
    this.focused = true;
  }

  onBlur() {
    this.focused = false;
  }

  search() {
    console.log('Searching for:', this.query);
  }
}

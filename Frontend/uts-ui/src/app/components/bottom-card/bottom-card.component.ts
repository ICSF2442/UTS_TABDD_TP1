import { Component } from '@angular/core';

@Component({
  selector: 'bottom-card',
  templateUrl: './bottom-card.component.html',
  styleUrls: ['./bottom-card.component.scss']
})
export class BottomCardComponent {
  expanded = false;

  toggleCard() {
    this.expanded = !this.expanded;
  }
}

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SearchBarComponent } from '../../components/search-bar/search-bar.component';
import { BottomCardComponent } from '../../components/bottom-card/bottom-card.component';
import { MapComponent } from '../../components/map/map.component';

@Component({
  selector: 'map-page',
  templateUrl: './map-page.component.html',
  imports: [SearchBarComponent,BottomCardComponent,MapComponent],
  styleUrls: ['./map-page.component.scss']
})
export class MapPageComponent {
  
}

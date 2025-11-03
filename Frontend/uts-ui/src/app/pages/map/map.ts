import { Component, OnInit, OnDestroy } from '@angular/core';
import * as L from 'leaflet';
import { Subscription } from 'rxjs';
import { TrackingService, VehiclePosition } from '../../core/services/tracking.service';

@Component({
  selector: 'app-map',
  standalone: true,
  templateUrl: './map.html',
  styleUrl: './map.scss'
})
export class MapComponent implements OnInit, OnDestroy {
  private map!: L.Map;
  private marker!: L.Marker;
  private sub!: Subscription;

  constructor(private trackingService: TrackingService) {}

  ngOnInit(): void {
    this.initMap();

    // Sub updates
    this.sub = this.trackingService.getVehiclePositions().subscribe((vehicles) => {
      const v = vehicles[0];
      if (this.marker) {
        this.marker.setLatLng([v.latitude, v.longitude]);
      } else {
        const icon = L.icon({
          iconUrl: 'https://cdn-icons-png.flaticon.com/512/194/194633.png',
          iconSize: [40, 40],
          iconAnchor: [20, 20]
        });
        this.marker = L.marker([v.latitude, v.longitude], { icon }).addTo(this.map);
      }
    });
  }

  private initMap(): void {
    this.map = L.map('map').setView([41.1579, -8.6291], 14);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);
  }

  ngOnDestroy(): void {
    if (this.sub) this.sub.unsubscribe();
  }
}

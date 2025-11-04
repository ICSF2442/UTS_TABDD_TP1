import { Component, OnInit, OnDestroy } from '@angular/core';
import * as L from 'leaflet';
import { Subscription, interval } from 'rxjs';
import { TrackingService, VehiclePosition } from '../../core/services/tracking.service';

@Component({
  selector: 'map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit, OnDestroy {
  private map!: L.Map;
  private metroMarker?: L.Marker;
  private sub?: Subscription;
  private animationFrame?: number;
  private lastUpdateTime = 0;
  private animStartPos?: [number, number];
  private animEndPos?: [number, number];
  private animStartTime?: number;
  private animDuration = 5000; // 5 seconds between positions

  private currentLat = 0;
  private currentLon = 0;

  private stops: [number, number][] = [
    [41.11556, -8.60653], // Santo Ovídio
    [41.11958, -8.60622], // D. João II
    [41.12611, -8.60569]  // João de Deus
  ];

  constructor(private trackingService: TrackingService) {}

  ngOnInit(): void {
    this.initMap();
    this.drawLineAndStops();

    this.sub = this.trackingService.getVehiclePositions().subscribe(vehicles => {
      const v = vehicles[0];
      if (!v) return;

      const newPos: [number, number] = [v.latitude, v.longitude];

      if (!this.metroMarker) {
        const metroIcon = L.icon({
          iconUrl: 'assets/metro-icon.png',
          iconSize: [40, 40],
          iconAnchor: [20, 20],
        });
        this.metroMarker = L.marker(newPos, { icon: metroIcon }).addTo(this.map);
        this.currentLat = newPos[0];
        this.currentLon = newPos[1];
        return;
      }

      this.animStartPos = [this.currentLat, this.currentLon];
      this.animEndPos = newPos;
      this.animStartTime = performance.now();

      this.animateMarker();

      this.currentLat = newPos[0];
      this.currentLon = newPos[1];
    });
  }

 private initMap() {
  const southWest = L.latLng(41.10, -8.62);  
  const northEast = L.latLng(41.13, -8.59);  
  const bounds = L.latLngBounds(southWest, northEast);

  this.map = L.map('map', {
    zoomControl: false,
    dragging: false, 
    scrollWheelZoom: true,
    doubleClickZoom: true,
    boxZoom: false,
    keyboard: false,
    maxBounds: bounds,          
    maxBoundsViscosity: 0.8
  }).setView([41.118, -8.606], 15);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 17,
    minZoom: 14
  }).addTo(this.map);

  this.map.setMaxBounds(bounds);
}

  private drawLineAndStops() {
    L.polyline(this.stops, { color: 'yellow', weight: 6 }).addTo(this.map);

    const stopNames = ['Santo Ovídio', 'D. João II', 'João de Deus'];
    this.stops.forEach(([lat, lon], i) => {
      L.circleMarker([lat, lon], {
        radius: 7,
        fillColor: '#ffcc00',
        color: '#000',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.95
      })
      .bindTooltip(stopNames[i], { permanent: true, direction: 'top' })
      .addTo(this.map);
    });
  }

  private animateMarker() {
    const animate = (now: number) => {
      if (!this.animStartTime || !this.animStartPos || !this.animEndPos) return;
      const elapsed = now - this.animStartTime;
      const t = Math.min(elapsed / this.animDuration, 1);
      const easeT = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; 

      const lat = this.animStartPos[0] + (this.animEndPos[0] - this.animStartPos[0]) * easeT;
      const lon = this.animStartPos[1] + (this.animEndPos[1] - this.animStartPos[1]) * easeT;

      this.metroMarker?.setLatLng([lat, lon]);

      if (t < 1) this.animationFrame = requestAnimationFrame(animate);
    };

    cancelAnimationFrame(this.animationFrame!);
    this.animationFrame = requestAnimationFrame(animate);
  }

  ngOnDestroy(): void {
    this.sub?.unsubscribe();
    if (this.animationFrame) cancelAnimationFrame(this.animationFrame);
  }
}

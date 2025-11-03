import { Injectable } from '@angular/core';
import { BehaviorSubject, interval } from 'rxjs';
import { map } from 'rxjs/operators';

export interface VehiclePosition {
  vehicle_id: number;
  line_id: number;
  latitude: number;
  longitude: number;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class TrackingService {
  private positions$ = new BehaviorSubject<VehiclePosition[]>([]);

  private routePoints = [
    [41.1579, -8.6291], // Trindade
    [41.1620, -8.6200], // Bolhão
    [41.1700, -8.6100], // Marquês
    [41.1750, -8.6000]  // Combatentes
  ];

  private index = 0;
  private direction = 1;

  constructor() {
    // a cada 5 segundos
    interval(5000).pipe(
      map(() => this.generateMockPosition())
    ).subscribe((pos) => this.positions$.next([pos]));
  }

  getVehiclePositions() {
    return this.positions$.asObservable();
  }

  //simular posicao, ate houver conexao com o redis
  private generateMockPosition(): VehiclePosition {
    this.index += this.direction;

    if (this.index >= this.routePoints.length - 1 || this.index <= 0) {
      this.direction *= -1;
    }

    const [lat, lon] = this.routePoints[this.index];

    return {
      vehicle_id: 1,
      line_id: 101,
      latitude: lat,
      longitude: lon,
      timestamp: new Date().toISOString()
    };
  }
}

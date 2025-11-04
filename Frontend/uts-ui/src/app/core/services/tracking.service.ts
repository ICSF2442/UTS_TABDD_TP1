import { Injectable } from '@angular/core';
import { BehaviorSubject, interval } from 'rxjs';
import { map } from 'rxjs/operators';

export interface VehiclePosition {
  id: string;
  latitude: number;
  longitude: number;
  timestamp: Date;
}

@Injectable({ providedIn: 'root' })
export class TrackingService {
  private positions$ = new BehaviorSubject<VehiclePosition[]>([]);

  // Metro D line - Gaia
  private lineD: [number, number][] = [
    [41.11556, -8.60653], // Santo Ovídio
    [41.11958, -8.60622], // D. João II
    [41.12611, -8.60569]  // João de Deus
  ];

  private index = 0;
  private direction = 1; 

  constructor() {
    interval(5000).pipe(
      map(() => {
        const pos = this.lineD[this.index];

        if (this.index === this.lineD.length - 1) this.direction = -1;
        else if (this.index === 0) this.direction = 1;

        this.index += this.direction;

        return [{
          id: 'metroD',
          latitude: pos[0],
          longitude: pos[1],
          timestamp: new Date()
        }];
      })
    ).subscribe((data) => this.positions$.next(data));
  }

  getVehiclePositions() {
    return this.positions$.asObservable();
  }
}

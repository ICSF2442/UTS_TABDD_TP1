import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BottomCardComponent } from './bottom-card.component';

describe('BottomCardComponent', () => {
  let component: BottomCardComponent;
  let fixture: ComponentFixture<BottomCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BottomCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BottomCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

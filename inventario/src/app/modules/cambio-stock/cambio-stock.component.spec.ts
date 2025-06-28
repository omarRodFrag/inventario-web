import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CambioStockComponent } from './cambio-stock.component';

describe('CambioStockComponent', () => {
  let component: CambioStockComponent;
  let fixture: ComponentFixture<CambioStockComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CambioStockComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CambioStockComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

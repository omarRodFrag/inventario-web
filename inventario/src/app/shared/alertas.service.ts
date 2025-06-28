import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ServiceService } from '../service.service';          // tu API service
import { Producto } from '../modules/login/interface/producto.interface';

@Injectable({ providedIn: 'root' })
export class AlertasService {
  private alertasCount = new BehaviorSubject<number>(0);
  alertasCount$ = this.alertasCount.asObservable();           // => se usará en la vista

  constructor(private api: ServiceService) {}

  /** Llama al backend y actualiza el contador */
  refrescar(): void {
    const token = localStorage.getItem('auth_token')!;
    this.api.obtenerProductos(token).subscribe({
      next: (productos: Producto[]) => {
        const n = productos.filter(p => p.activo && p.cantidad <= p.stockMinimo).length;
        this.alertasCount.next(n);
      },
      error: () => this.alertasCount.next(0)
    });
  }
}

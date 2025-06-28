import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../../service.service';
import { Producto } from '../login/interface/producto.interface';

@Component({
  selector: 'app-alertas',
  standalone: false,
  templateUrl: './alertas.component.html',
  styleUrl: './alertas.component.css'
})
export class AlertasComponent {
  alertas: Producto[] = [];

  constructor(private service: ServiceService) {}

  ngOnInit(): void {
    const token = localStorage.getItem('auth_token')!;
    this.service.obtenerProductos(token).subscribe({
      next: (productos) => {
        this.alertas = productos.filter(p => p.cantidad <= p.stockMinimo && p.activo);
      }
    });
  }

}

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServiceService } from '../../service.service';
import Swal from 'sweetalert2';
import { Producto } from '../login/interface/producto.interface';
import { AlertasService } from '../../shared/alertas.service';

@Component({
  selector: 'app-inventario',
  standalone: false,
  templateUrl: './inventario.component.html',
  styleUrl: './inventario.component.css'
})
export class InventarioComponent {
  searchTerm: string = '';
  productos: Producto[] = [];

  constructor(
    private router: Router,
    private service: ServiceService,
    private alertasService: AlertasService 
  ) {}

  ngOnInit(): void {
    this.cargarProductos();
  }

  cargarProductos(): void {
    const token = localStorage.getItem('auth_token')!;
    this.service.obtenerProductos(token).subscribe({
      next: (data) => {
        this.productos = data;
        this.alertasService.refrescar();
      },
      error: () => {
        Swal.fire('Error', 'No se pudieron cargar los productos', 'error');
        this.router.navigate(['/login']);
      }
    });
  }

  cambiarStatus(producto: Producto) {
  const token = localStorage.getItem('auth_token')!;
  const estadoNuevo = producto.activo;

  this.service.actualizarEstadoProducto(
    producto.idProducto!, 
    estadoNuevo,
    token
  ).subscribe({
    next: () => {
      // Éxito: si quieres, muestra un toast
      this.alertasService.refrescar(); 
      Swal.fire('Hecho', 'El Status a sido actualizado', 'success');
    },
    error: () => {
      producto.activo = !estadoNuevo;
      Swal.fire('Error', 'No se pudo actualizar el status', 'error');
    }
  });
}

  productosFiltrados() {
    return this.productos.filter(p =>
      p.nombre.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  agregarProducto() {
    this.router.navigate(['/productos/agregar']);
  }

  editarProducto(producto: Producto) {
    this.router.navigate(['/productos/editar', producto.idProducto]);
  }
  ajustarStock(producto: Producto) {
  this.router.navigate(['/productos/stock', producto.idProducto]);
}

  eliminarProducto(producto: Producto) {
    const confirmar = confirm(`¿Eliminar ${producto.nombre}?`);
    if (!confirmar || !producto.idProducto) return;

    const token = localStorage.getItem('auth_token')!;
    this.service.eliminarProducto(producto.idProducto, token).subscribe({
      next: () => {
        Swal.fire('Eliminado', 'Producto eliminado correctamente', 'success');
        this.cargarProductos(); // recargar lista
      },
      error: () => {
        Swal.fire('Error', 'No se pudo eliminar el producto', 'error');
      }
    });
  }
}

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServiceService } from '../../service.service';
import Swal from 'sweetalert2';
import { Producto } from '../login/interface/producto.interface';

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
    private service: ServiceService
  ) {}

  ngOnInit(): void {
    this.cargarProductos();
  }

  cargarProductos(): void {
    const token = localStorage.getItem('auth_token')!;
    this.service.obtenerProductos(token).subscribe({
      next: (data) => {
        this.productos = data;
      },
      error: () => {
        Swal.fire('Error', 'No se pudieron cargar los productos', 'error');
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
    this.router.navigate(['/productos/editar', producto._id]);
  }

  eliminarProducto(producto: Producto) {
    const confirmar = confirm(`¿Eliminar ${producto.nombre}?`);
    if (!confirmar || !producto._id) return;

    const token = localStorage.getItem('auth_token')!;
    this.service.eliminarProducto(producto._id, token).subscribe({
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

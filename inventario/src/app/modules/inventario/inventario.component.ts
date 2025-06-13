import { Component } from '@angular/core';

@Component({
  selector: 'app-inventario',
  standalone: false,
  templateUrl: './inventario.component.html',
  styleUrl: './inventario.component.css'
})
export class InventarioComponent {
  searchTerm: string = '';
  productos = [
    { nombre: 'Producto 1', cantidad: 10, activo: true },
    { nombre: 'Producto 2', cantidad: 3, activo: false },
    { nombre: 'Producto 3', cantidad: 7, activo: true },
    { nombre: 'Producto 4', cantidad: 12, activo: true },
    { nombre: 'Producto 5', cantidad: 1, activo: false },
    { nombre: 'Producto 6', cantidad: 5, activo: true }
  ];

  productosFiltrados() {
    return this.productos.filter(p =>
      p.nombre.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  agregarProducto() {
    alert('Agregar producto');
  }

  editarProducto(producto: any) {
    alert(`Editar ${producto.nombre}`);
  }

  eliminarProducto(producto: any) {
    const confirmacion = confirm(`¿Eliminar ${producto.nombre}?`);
    if (confirmacion) {
      this.productos = this.productos.filter(p => p !== producto);
    }
  }
}

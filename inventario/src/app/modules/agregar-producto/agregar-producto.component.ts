import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ServiceService } from '../../service.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-agregar-producto',
  standalone: false,
  templateUrl: './agregar-producto.component.html',
  styleUrl: './agregar-producto.component.css'
})
export class AgregarProductoComponent {
  productoForm!: FormGroup;
  modoEdicion: boolean = false;
  productoId: string | null = null;

  constructor(
    private fb: FormBuilder,
    private service: ServiceService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.productoForm = this.fb.group({
      nombre: ['', Validators.required],
      categoria: ['', Validators.required],
      descripcion: [''],
      cantidad: [0, [Validators.required, Validators.min(0)]],
      stockMinimo: [0, [Validators.required, Validators.min(0)]],
      activo: [true]
    });

    this.productoId = this.route.snapshot.paramMap.get('id');
    this.modoEdicion = !!this.productoId;

    if (this.modoEdicion && this.productoId) {
      const token = localStorage.getItem('auth_token')!;
      this.service.obtenerProductoPorId(this.productoId, token).subscribe({
        next: (producto) => {
          this.productoForm.patchValue(producto);
        },
        error: () => {
          Swal.fire('Error', 'No se pudo cargar el producto.', 'error');
          this.router.navigate(['/inventario']);
        }
      });
    }
  }

  guardar(): void {
    if (this.productoForm.invalid) {
      Swal.fire('Formulario inválido', 'Revisa los campos', 'warning');
      return;
    }

    const token = localStorage.getItem('auth_token')!;
    const producto = this.productoForm.value;

    if (this.modoEdicion && this.productoId) {
      this.service.actualizarProducto(this.productoId, producto, token).subscribe({
        next: () => {
          Swal.fire('Actualizado', 'Producto actualizado correctamente', 'success');
          this.router.navigate(['/inventario']);
        },
        error: () => {
          Swal.fire('Error', 'No se pudo actualizar el producto', 'error');
        }
      });
    } else {
      console.log('TOKEN QUE SE ENVÍA:', token);
      this.service.agregarProducto(producto, token).subscribe({
        next: () => {
          Swal.fire('Agregado', 'Producto agregado correctamente', 'success');
          this.router.navigate(['/inventario']);
        },
        error: () => {
          Swal.fire('Error', 'No se pudo agregar el producto', 'error');
        }
      });
    }
  }

  cancelar(): void {
    this.router.navigate(['/inventario']);
  }
}

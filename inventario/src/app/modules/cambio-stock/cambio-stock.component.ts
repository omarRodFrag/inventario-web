import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ServiceService } from '../../service.service';
import Swal from 'sweetalert2';
import { AlertasService } from '../../shared/alertas.service';

@Component({
  selector: 'app-cambio-stock',
  standalone: false,
  templateUrl: './cambio-stock.component.html',
  styleUrl: './cambio-stock.component.css'
})
export class CambioStockComponent {
  stockForm!: FormGroup;
  productoId!: string;

  constructor(
    private fb: FormBuilder,
    private service: ServiceService,
    private route: ActivatedRoute,
      private alertasService: AlertasService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.stockForm = this.fb.group({
      cantidad: [0, [Validators.required, Validators.min(0)]],
      stockMinimo: [0, [Validators.required, Validators.min(0)]]
    });

    this.productoId = this.route.snapshot.paramMap.get('id')!;
    const token = localStorage.getItem('auth_token')!;
    this.service.obtenerProductoPorId(this.productoId, token).subscribe({
      next: (producto) => {
        this.stockForm.patchValue({
          cantidad: producto.cantidad,
          stockMinimo: producto.stockMinimo
        });
      },
      error: () => {
        Swal.fire('Error', 'No se pudo cargar el stock', 'error');
        this.router.navigate(['/inventario']);
      }
    });
  }

  guardar(): void {
    if (this.stockForm.invalid) {
      this.stockForm.markAllAsTouched();
      return;
    }

    const token = localStorage.getItem('auth_token')!;
    // Para actualizar solo stock, envías esos campos
    this.service.actualizarProducto(this.productoId, this.stockForm.value, token)
      .subscribe({
        next: () => {
          this.alertasService.refrescar(); 
          Swal.fire('Éxito', 'Stock actualizado correctamente', 'success');
          this.router.navigate(['/inventario']);
        },
        error: () => Swal.fire('Error', 'No se pudo actualizar el stock', 'error')
      });
  }

  cancelar(): void {
    this.router.navigate(['/inventario']);
  }

  get c() { return this.stockForm.controls; }

}

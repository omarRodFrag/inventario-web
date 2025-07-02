import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { Observable } from 'rxjs';
import { AlertasService } from '../alertas.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  standalone: false
})
export class NavbarComponent implements OnInit {
  alertasCount$!: Observable<number>;

  constructor(
    private alertasService: AlertasService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.alertasCount$ = this.alertasService.alertasCount$;
    this.alertasService.refrescar();
  }

  /** Pregunta y cierra sesión */
  confirmLogout(): void {
    Swal.fire({
      title: 'Cerrar sesión',
      text: '¿Seguro que quieres salir?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Salir',
      cancelButtonText: 'Cancelar'
    }).then(res => {
      if (res.isConfirmed) {
        localStorage.removeItem('auth_token');   // limpia el JWT
        this.router.navigate(['/login']);        // regresa al login
      }
    });
  }
}

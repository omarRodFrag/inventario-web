import { Component, OnInit } from '@angular/core';
import { AlertasService } from '../alertas.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  standalone:false
})
export class NavbarComponent implements OnInit {
  alertasCount$!: Observable<number>;  // <- declara sin inicializar

  constructor(private alertasService: AlertasService) {}

  ngOnInit(): void {
    this.alertasCount$ = this.alertasService.alertasCount$; // <- ya inicializado
    this.alertasService.refrescar();
  }
}
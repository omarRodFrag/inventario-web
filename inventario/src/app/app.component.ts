import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Inventrack';
  showNavbar = true;                          // ← se actualiza en cada navegación

  // Rutas en las que NO quieres navbar
  private rutasSinNavbar = ['/login'];

  constructor(private router: Router) {
    // Cada vez que cambia la URL revisamos si debemos ocultar
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        this.showNavbar = !this.rutasSinNavbar.includes(event.urlAfterRedirects);
      });
  }
}

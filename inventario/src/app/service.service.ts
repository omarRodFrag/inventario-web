import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Producto } from './modules/login/interface/producto.interface';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  private baseUrl = 'https://inventario-back-bmrw.onrender.com'; // URL base de tu backend

  constructor(private http: HttpClient) { }

  // Login con JWT
  login(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, data);
  }

  // Verificar el código de verificación
  verifyCode(body: { code: string }, headers: HttpHeaders): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/verify`, body, { headers });
  }

  obtenerProductoPorId(id: string, token: string): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get(`${this.baseUrl}/productos/${id}`, { headers });
  }

  agregarProducto(producto: any, token: string): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.post(`${this.baseUrl}/productos/agregar`, producto, { headers });
  }

  actualizarProducto(id: string, producto: any, token: string): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.put(`${this.baseUrl}/productos/actualizar/${id}`, producto, { headers });
  }
  obtenerProductos(token: string): Observable<Producto[]> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<Producto[]>(`${this.baseUrl}/productos`, { headers });
  }

  eliminarProducto(id: number, token: string): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.delete(`${this.baseUrl}/productos/eliminar/${id}`, { headers });
  }

  actualizarEstadoProducto(id: number, activo: boolean, token: string) {
  const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
  // PATCH si creas un endpoint nuevo; PUT si reutilizas el existente
  return this.http.patch(
    `${this.baseUrl}/productos/estado/${id}`,
    { activo },
    { headers }
  );
}
}

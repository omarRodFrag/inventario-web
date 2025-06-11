import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

   private baseUrl = 'http://localhost:5000'; // URL base de tu backend

  constructor(private http: HttpClient) { }

  // Login con JWT
  login(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, data);
  }

  // Verificar el código de verificación
  verifyCode(body: { email: string, code: string }, headers: HttpHeaders): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/verify`, body, { headers });
  }
}

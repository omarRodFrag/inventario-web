import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './modules/login/login.component';
import { InventarioComponent } from './modules/inventario/inventario.component';
import { AgregarProductoComponent } from './modules/agregar-producto/agregar-producto.component';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'inventario', component: InventarioComponent },
  { path: 'productos/agregar', component: AgregarProductoComponent },
  { path: 'productos/editar/:id', component: AgregarProductoComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './modules/login/login.component';
import { InventarioComponent } from './modules/inventario/inventario.component';
import { AgregarProductoComponent } from './modules/agregar-producto/agregar-producto.component';
import { CambioStockComponent } from './modules/cambio-stock/cambio-stock.component';
import { AlertasComponent } from './modules/alertas/alertas.component';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'inventario', component: InventarioComponent },
  { path: 'productos/agregar', component: AgregarProductoComponent },
  { path: 'productos/editar/:id', component: AgregarProductoComponent },
  { path: 'productos/stock/:id', component: CambioStockComponent },
  { path: 'productos/alertas', component: AlertasComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

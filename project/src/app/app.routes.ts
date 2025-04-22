import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { CartComponent } from './cart/cart.component';
import { ProductDetailsComponent } from './product-details/product-details.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';

export const routes: Routes = [
    { path: '', redirectTo: 'main', pathMatch: 'full' },
    { path: 'main', component: HomeComponent, title: 'Главная страница' },
    { path: 'cart', component: CartComponent, title: 'Корзина' },
    {path: 'category/:categoryId',component: ProductDetailsComponent, title: 'Все продукты товара' },
    {path: 'login',component: LoginComponent, title: 'Логин' },
    {path: 'register',component: RegisterComponent, title: 'Регистрация' },
];

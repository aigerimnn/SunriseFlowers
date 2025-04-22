import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Category, Product } from './models';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(private client: HttpClient) { }

  getCategories(): Observable<Category[]> {
    return this.client.get<Category[]>(`http://127.0.0.1:8000/flower/categories/`);
  }
  getProductsByCategoryId(categoryId: number): Observable<Product[]> {
    return this.client.get<Product[]>(`http://127.0.0.1:8000/flower/products/?category_id=${categoryId}`);
  }
}

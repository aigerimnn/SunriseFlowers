import { Component, OnInit } from '@angular/core';
import { Category, Product } from '../models';
import { ActivatedRoute } from '@angular/router';
import { AppService } from '../app.service';
import { CommonModule } from '@angular/common';
import { CartService } from '../cart.service';

@Component({
  selector: 'app-product-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-details.component.html',
  styleUrl: './product-details.component.css'
})
export class ProductDetailsComponent implements OnInit {
  products : Product[] = [];
  //categoryName: string | null = null;

  constructor(private route: ActivatedRoute, private appService: AppService, private cartService: CartService ) {}
  
  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const categoryId = Number(params.get('categoryId'));
      this.appService.getProductsByCategoryId(categoryId).subscribe(
        products => {
          this.products = products
        }
      )
   
    });
  }


  addToCart(product: Product): void {
    this.cartService.addToCart(product).subscribe({
      next: (response) => {
        console.log('Product added to cart:', response);
        // Optionally, update UI or local state here
      },
      error: (error) => {
        console.error('Failed to add product to cart:', error);
        // Handle errors (e.g., show error message to user)
      }
    });
  }

}

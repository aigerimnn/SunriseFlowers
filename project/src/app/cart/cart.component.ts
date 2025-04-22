import { Component, OnInit } from '@angular/core';
import { CartItem, Product } from '../models';
import { CartService } from '../cart.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.css'
})
export class CartComponent implements OnInit {
  items: CartItem[] = [];

  constructor(private cartService: CartService) { }

  ngOnInit(): void {
    this.cartService.getItems().subscribe({
      next: (items) => this.items = items,
      error: (error) => console.error('Error fetching cart items', error)
    });
  } 
  checkout(): void {
    this.cartService.checkout().subscribe({
      next: (response) => {
        alert("Checkout successful");
        console.log('Checkout successful:', response);
      },
      error: (error) => {
        alert("Checkout failed");
        console.error('Checkout failed:', error);
      }
    });
  }

}
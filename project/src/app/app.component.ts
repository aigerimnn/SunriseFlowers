
import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { Category } from './models';
import { CartComponent } from './cart/cart.component';
import { HttpClientModule } from '@angular/common/http';
import { AppService } from './app.service';
import { Emitters } from './emitters/emitters';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true, 
  imports: [RouterOutlet, RouterModule, HomeComponent, HttpClientModule, CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent  implements OnInit {
  title = 'project';
  isLoggedIn: boolean = false;


  constructor(private router: Router, private cookieService: CookieService) {
    this.checkLoginStatus();
  }

  ngOnInit(): void {
    
  }

  checkLoginStatus(): void {
    this.isLoggedIn = this.cookieService.check('access_token');
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.cookieService.delete('access_token');
    this.cookieService.delete('refresh_token');
    this.isLoggedIn = false;
    this.router.navigate(['/']); // Redirect to home page or login
  }

  openWhatsAppLink() {
    const link = "https://wa.me/77471123012";
    window.open(link, '_blank');
}

  openInstagram() {
    const instagramUrl = "https://www.instagram.com/sunrise_flowers_uralsk?igsh=NTFqMXlpM3VmbHk4";
    window.open(instagramUrl, '_blank');

  }

}

import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators, ReactiveFormsModule} from '@angular/forms';
import { AuthService } from '../auth.service';
import { Emitters } from '../emitters/emitters';
import { CookieService } from 'ngx-cookie-service';
import { Router, NavigationExtras } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent implements OnInit {
  form: FormGroup;

  constructor(private formBuilder: FormBuilder, private authService: AuthService, private cookieService: CookieService, private router: Router){
    this.form = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      password_new: ['', Validators.required]
    });
  }

  ngOnInit(): void {

  }

  submit(): void {
    if (this.form.valid && this.form.value.password === this.form.value.password_new) {
      this.authService.registerFunc(this.form).subscribe({
        next: ()=>{
          // Pass a success message to the /login route
          const navigationExtras: NavigationExtras = {
            queryParams: { registrationSuccess: true }
          };
          this.router.navigate(['/login'], navigationExtras);
        }
      })
    } else {
      if (this.form.value.password !== this.form.value.password_new) {
        alert('Passwords do not match!');
      }
    }
  }

}

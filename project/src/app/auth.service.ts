import { Injectable } from '@angular/core';
import {FormBuilder, FormGroup} from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
    private auth_url = `http://127.0.0.1:8000/flower/login/`;
    private register_url = `http://127.0.0.1:8000/flower/register/`;

    constructor(private http: HttpClient) {
    
    }

    authFunc(form: FormGroup): Observable<any> {
        return this.http.post(this.auth_url, form.getRawValue(), {
            withCredentials: true,
        });
    }

    registerFunc(form: FormGroup): Observable<any> {
        return this.http.post(this.register_url, form.getRawValue(), {
            withCredentials: true,
        });
    }
}
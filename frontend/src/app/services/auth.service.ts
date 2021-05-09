import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type':'application/json'
    })
}

@Injectable({ providedIn: 'root' })
export class AuthService {
    isUserLoggedIn: boolean = false;
    api_url: string = 'http://localhost:8000/';
    constructor(private http: HttpClient) { }

    login(email: string, password: string) {
        console.log("Login called")
        return this.http.post<any>(this.api_url + `login/`, { email, password }, httpOptions)
            .pipe(map(user => {
                if (user && user.token) {
                    console.log("saving data into local storage")
                    localStorage.setItem('token', user.token);
                    localStorage.setItem('userId', user.user.id);
                    localStorage.setItem('username', user.user.email);
                    localStorage.setItem('email', user.user.email);
                    localStorage.setItem('name', user.user.first_name+" "+user.user.last_name);
                    this.isUserLoggedIn = true;
                    localStorage.setItem('isUserLoggedIn', this.isUserLoggedIn ? "true" : "false");
                    console.log("data saved")
                }
                return user;
            })
        );
    }
 
    logout() {
        // remove user from local storage and set current user to null
        localStorage.removeItem('token');
        this.isUserLoggedIn = false;
        localStorage.removeItem('isUserLoggedIn'); 
        localStorage.removeItem('userId');
        localStorage.removeItem('username');
        localStorage.removeItem('email');
        localStorage.removeItem('name');
    }
}

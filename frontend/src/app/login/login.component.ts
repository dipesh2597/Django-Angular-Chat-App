import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  
  // error messages received from the login attempt
  public errors: any = [];
  loginForm!: FormGroup;
  constructor( private authService: AuthService, private router: Router) { }

  ngOnInit(): void {
      this.loginForm = new FormGroup({
          email: new FormControl(''),
          password: new FormControl('')
      });
  }
  
  get form(){
      return this.loginForm.controls;
  }

  onSubmit() {
      console.log("Button Clicked")
      this.authService.login(this.form.email.value,this.form.password.value).pipe(first()).subscribe(
          data => {
              this.router.navigate(['message/'])
          },
          err => {
              console.log(err['error']['message'])
              this.errors = err['error']['message'];
          }
      )
  }
}

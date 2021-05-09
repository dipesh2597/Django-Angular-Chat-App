import { Component } from '@angular/core';
import { ChatService} from './services/chat.service';
import { Router } from '@angular/router';
import {AuthService} from './services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Chat App';
  displayLogOut: boolean = false;
  constructor( private cService: ChatService, public authService: AuthService, private router: Router) {

  }
  ngOnInit(): void {
      if (localStorage.getItem('token') !== null){
        this.router.navigate(['message/'])
        this.displayLogOut=true;
      }
      else {
        this.router.navigate(['login/'])
      }
      console.log(this.displayLogOut)
  }

}

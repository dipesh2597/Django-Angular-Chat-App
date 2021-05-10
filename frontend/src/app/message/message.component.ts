import { Component, OnInit, Renderer2 } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl } from '@angular/forms';
import { ChatService } from '../services/chat.service';
import {AuthService} from '../services/auth.service';
import { first } from 'rxjs/operators';

export interface Message {
  author: string;
  message: string;
}


@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.scss']
})
export class MessageComponent implements OnInit {
  public ws:any;
  private httpOptions:any = { };
  msgForm!: FormGroup;
  public users:any = [];
  public errors: any = [];
  res:any;
  public messages:any = [];
  myWebSocket:any;
  message='';
  session_uuid:any;
  public selectedUser:any;
  public selectedUserId:any;
  public userName:any;
  displayLogOut: boolean = false;
  constructor(private cService: ChatService,private authService: AuthService,private router: Router,private renderer:Renderer2) { }
  
  ngOnInit(): void {
      if (localStorage.getItem('token') !== null){
        this.router.navigate(['message/'])
        this.displayLogOut=true;
      }
      this.userName=localStorage.getItem('name');
      this.showOnlineUsers();
      this.msgForm = new FormGroup({
          message: new FormControl('')
      });
      
  }

  setClasses(userId:any) {
    if (userId==this.selectedUserId){
        var isActive=true;
    }
    else {
        var isActive = false
    }
    let classes = {
        active: isActive,
    };
    return classes;
  }

  getClasses(msgType:any) {
    if (msgType=="sent"){
        var isSent=true;
        var isRecieved=false;
    }
    else {
        var isSent=false;
        var isRecieved = true;
    }
    let classes = {
        ongoing: isSent,
        incoming: isRecieved,
    };
    return classes;
  }

  showOnlineUsers() {
          this.cService.getOnlineUsersList().subscribe(data => {
          this.users = data;
          this.selectedUser=this.users[0];
          console.log(this.selectedUser,this.selectedUser.username)
          this.selectedUserId=this.users[0].user_id;
          this.showMessage()
      });
      
  }

  showMessage() {
          var self = this; //decalring this self = this so that can user this self to push messages recieving thourhg websocket
          this.cService.getMessage(this.selectedUserId).subscribe(data => {
          this.res = data;
          this.messages = this.res['message']
          this.session_uuid = this.res['current_session_uuid']
          // connecting to WebSocket
          this.ws = new WebSocket("ws://127.0.0.1:8000/"+this.session_uuid+"/");
          console.log("checking web socket for new messages")
          this.ws.onmessage = function(e:any,messages:any) {
                var msg_data = JSON.parse(e.data);
                var current_user_id = localStorage.getItem('userId');
                if (current_user_id == msg_data['userid']){
                    var msg_type='sent';
                } 
                else {
                    var msg_type = 'recieved'
                }
                self.messages.push({"message":msg_data['text'],"msg_type":msg_type})
            }
        
      });
  }

  get form(){
      return this.msgForm.controls;
  }

  sendMessage() {
      this.cService.sendMessage(this.form.message.value,this.session_uuid).pipe(first()).subscribe(
          data => {
              console.log("sedning message into websocket", this.ws)
              this.ws.send(JSON.stringify({"text":this.form.message.value,"userid":localStorage.getItem('userId')}));
              console.log("message sent")
              this.msgForm.reset();
          },
          err => {
              this.errors = err['error']['message'];
          }
      )
      console.log('sendMessage called')
  }

  switchChat (userId:string) {
      console.log("switchChat Called for user",userId)
      this.selectedUserId = userId;
      for (var i = 0; i < this.users.length; i++){
            var obj = this.users[i];
            console.log(obj,userId,obj['user_id'])
            if (obj['user_id']==userId){
                this.selectedUser=obj;
            }
        }
      this.cService.getMessage(userId).subscribe(data => {
          this.res = data;
          this.messages = this.res['message']
          this.session_uuid = this.res['current_session_uuid']
      })
  }
  logout() {
      this.authService.logout();
      this.displayLogOut=false;
      this.router.navigate(['login/'])
  }
}

import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { Observable, Subject } from "rxjs/Rx";


@Injectable({
  providedIn: 'root'
})

export class ChatService {
  private httpOptions:any = { };
  public users:any = [];
  api_url='http://localhost:8000/';
  constructor(private http: HttpClient) { }

  getMessage(userId: string) {
      this.httpOptions = {
          headers: {
            'Authorization': 'Token '+localStorage.getItem('token')
            }
      }
      return this.http.get(this.api_url+'get-messages/'+userId+'/',this.httpOptions);
  }

  getOnlineUsersList()   {
      this.httpOptions = {
          headers: {
            'Authorization': 'Token '+localStorage.getItem('token')
            }
      }
      return this.http.get(this.api_url+'get-online-users/',this.httpOptions)
  }

  sendMessage(message:string,session_uuid:string) {
      this.httpOptions = {
          headers: {
            'Authorization': 'Token '+localStorage.getItem('token')
            }
      }
      return this.http.post(this.api_url+'send-message/'+session_uuid+"/",{message},this.httpOptions)
  }
}

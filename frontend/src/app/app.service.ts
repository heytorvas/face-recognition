import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { API } from './app.api'

@Injectable({
  providedIn: 'root'
})

export class AppService {

    constructor(private http: HttpClient) {}
  
    public uploadImage(image: File): Observable<Response> {
      const formData = new FormData();
  
      formData.append('image', image);
  
      return this.http.post<any>(`${API}upload-image`, formData);
    }
}

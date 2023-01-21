import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { environment } from '../../environments/environment';
import { User } from '../_models';
import { JwtInterceptor } from '../_helpers';
import { catchError } from 'rxjs/operators';
// import { userInfo } from 'os';

@Injectable()
export class UserService {
    constructor(private http: HttpClient) { }
    
    baseUrl: String = 'http://localhost:8000/';

    getAll() {
        return this.http.get<User[]>(`${environment.apiUrl}/users`);
    }

    getById(id: number) {
        return this.http.get(`${environment.apiUrl}/users/` + id);
    }

    register(user: User) {
        return this.http.post(`${environment.apiUrl}/users/register`, user);
    }

    update(user: User) {
        return this.http.put(`${environment.apiUrl}/users/` + user.id, user);
    }

    delete(id: number) {
        return this.http.delete(`${environment.apiUrl}/users/` + id);
    }

    loginUser(user){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS,DELETE,PUT',
          });
        return this.http.post<any>(this.baseUrl+`UserLogin`, user, { headers: headers })
    }

    registerUser(user){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
          });
          return this.http.post<any>(this.baseUrl+`Register`, user, { headers: headers })
    }

    getAllUserFileData(){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.get<any>(this.baseUrl+`getAllUserFileData`);
    }

    getAllUserFileDataByUserId(id){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.get<any>(this.baseUrl+`GetUserFileDataByUserId?userid=`+id);
    }

    downloadFile(obj){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
          });
          return this.http.post<any>(this.baseUrl+`RetriveFile`, obj, { headers: headers });
    }

    getUserByUserId(id){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.get<any>(this.baseUrl+`GetUserById?userid=`+id);
    }

    getAllAdminFileRequests(){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.get<any>(this.baseUrl+`getalladminfilerequest`);
    }

    deleteAdminFileRequest(obj){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.post<any>(this.baseUrl+`deletefilerequest`, obj, { headers: headers });
    }

    checkGuestDownloadTimer(id){
        return this.http.get<any>(this.baseUrl+`guestchecktimer?id=`+id);
    }

    addFileRequestToAdmin(obj){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.post<any>(this.baseUrl+`AddFileRequestToAdmin`, obj, { headers: headers });
    }

    deleteUserFile(obj){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.post<any>(this.baseUrl+`deletefilerequestbyuser`, obj, { headers: headers });
    }

    acceptFileRequest(obj){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
        });
        return this.http.post<any>(this.baseUrl+`sendfilerequest`, obj, { headers: headers });
    }

    uploadfile(obj){
        let headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8000',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS',
          });
          return this.http.post<any>(this.baseUrl+`UploadFile`, obj, { headers: headers });
    }
    
}
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import Swal from 'sweetalert2';
import { UserService } from '../_services';

@Component({
  selector: 'app-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.css']
})
export class FileComponent implements OnInit {
  private routeSub: Subscription;
  fileId : any;
  ipAddress = '';

  constructor(private route: ActivatedRoute,
    private userService: UserService,
    private router: Router,
    private http: HttpClient) { }

  ngOnInit() {
    this.routeSub = this.route.params.subscribe(params => {
      console.log(params) //log the entire params object
      console.log(params['id']) //log the value of id
      this.fileId = params['id'];
      this.http.get("http://api.ipify.org/?format=json").subscribe((res:any)=>{
        this.ipAddress = res.ip;
        let dataSave = {
          "id": this.ipAddress,
          "fileId": this.fileId,
        }
        this.userService.downloadFile(dataSave).subscribe(data => {
          console.log(data);
          Swal.fire("File Downloaded Successfully. Now you can download next file after 10 minutes.")
        }) 
      })
    })
  }
}

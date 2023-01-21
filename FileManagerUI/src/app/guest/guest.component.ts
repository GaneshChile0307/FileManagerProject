import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import Swal from 'sweetalert2';
import { UserService } from '../_services';

@Component({
  selector: 'app-guest',
  templateUrl: './guest.component.html',
  styleUrls: ['./guest.component.css']
})
export class GuestComponent implements OnInit {

  private routeSub: Subscription;
  currentUserName: String;
  userId : String;
  ipAddress = '';
  fileDatas: any = [
    {
      "id":1,
      "name": "test1.txt",
      "status":"Blocked",
      "creationDate":"17 May 2022 18:28:30",
      "updationDate":"17 May 2022 18:28:30",
      "size": "280 Kb"
    },
    {
      "id":2,
      "name": "test2.txt",
      "status":"Unblocked",
      "creationDate":"17 May 2022 18:28:30",
      "updationDate":"17 May 2022 18:28:30",
      "size": "280 Kb"
    },
    {
      "id":3,
      "name": "test3.txt",
      "status":"Blocked",
      "creationDate":"17 May 2022 18:28:30",
      "updationDate":"17 May 2022 18:28:30",
      "size": "280 Kb"
    },
    {
      "id":3,
      "name": "test3.txt",
      "status":"Blocked",
      "creationDate":"17 May 2022 18:28:30",
      "updationDate":"17 May 2022 18:28:30",
      "size": "280 Kb"
    },
    {
      "id":3,
      "name": "test3.txt",
      "status":"Blocked",
      "creationDate":"17 May 2022 18:28:30",
      "updationDate":"17 May 2022 18:28:30",
      "size": "280 Kb"
    }
  ];
  constructor(private route: ActivatedRoute,
    private userService: UserService,
    private router: Router,
    private http: HttpClient) { }

  ngOnInit() {
    this.userService.getAllUserFileData().subscribe( data => {
      console.log(data);
      if(data.status == 'success'){
        this.fileDatas = data.userDetails;
      }
    })
  }

  downloadFile(fid){
    this.http.get("http://api.ipify.org/?format=json").subscribe((res:any)=>{
    this.ipAddress = res.ip;
    let dataSave = {
      "id": this.ipAddress,
      "fileId": fid,
    }
    console.log(dataSave);
    this.userService.checkGuestDownloadTimer(this.ipAddress)
      .subscribe(data => {
        
        if(data.status == "success"){
          this.userService.downloadFile(dataSave).subscribe(data => {
          console.log(data);
          Swal.fire("File Downloaded Successfully. Now you can download next file after 10 minutes.")
        })
      }
      else{
        let sec = data.time%60;
        let min = data.time/60;
        Swal.fire("You have to wait for "+min+" minutes and "+sec+" seconds for the next download. Thanks for your patience.");
      }
 
      })
  });
 }

  BackButton(){
    this.router.navigate(['login'])
  }

}

import { Component, OnInit , Injectable} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { UserService } from '../_services';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})

export class AdminComponent implements OnInit {
  private routeSub: Subscription;
  currentUserName: String;
  adminId: String
  userId: any;
  fileDatas: any = [
    {
      "id":1,
      "userName": "Anjali Gupta",
      "userEmail": "anjali@kuchbhi.in",
      "name":"test1.txt",
      "size": "280 Kb",
      "requestMessage": "Blocked the file"
    },
    {
      "id":1,
      "userName": "Ganesh Chile",
      "userEmail": "ganesh@kuchbhi.in",
      "name":"test2.txt",
      "size": "180 Kb",
      "requestMessage": "Unblocked the file"
    },
    {
      "id":1,
      "userName": "Ashish Pathak",
      "userEmail": "ashish@kuchbhi.in",
      "name":"test3.txt",
      "size": "330 Kb",
      "requestMessage": "Blocked the file"
    }
  ]
    
  constructor(private route: ActivatedRoute,
    private userService: UserService,
    private router: Router) { }
  
  
  ngOnInit(): void {
    this.routeSub = this.route.params.subscribe(params => {
      console.log(params) //log the entire params object
      console.log(params['id']) //log the value of id
      this.userId = params['id'];
      this.userService.getUserByUserId(this.userId)
        .subscribe(
          data => {
            console.log(data)
            this.currentUserName = data.userDetails.userName
            console.log(this.currentUserName)
          }
        )

      this.userService.getAllAdminFileRequests()
        .subscribe(data => {
          console.log(data);
          this.fileDatas = data.data;
        })
    });
  }

  acceptRequest(reqId){
    let data = {
      "reqId" : reqId 
    }
    this.userService.acceptFileRequest(data)
      .subscribe( data => {
      if(data.status == "success"){
        Swal.fire(data.msg);
      }
      this.ngOnInit();
    })
  }

  declineRequest(rid){
    let data = {
      "requestId": rid
    }
    console.log(data);

    this.userService.deleteAdminFileRequest(data)
      .subscribe( data => {
        console.log(data);
        Swal.fire('Request Declined Successfully');
        this.ngOnInit();
      })
  }

  BackButton(){
    this.router.navigate(['login'])
  }

}

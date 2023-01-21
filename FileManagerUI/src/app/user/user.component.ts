import { analyzeAndValidateNgModules } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { toInteger } from '@ng-bootstrap/ng-bootstrap/util/util';
import { Subscription } from 'rxjs';
import Swal from 'sweetalert2';
import { UserService } from '../_services';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  private routeSub: Subscription;
  currentUserName: String;
  userId : any;
  userEmail : any;
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
    }
  ];
  constructor(private route: ActivatedRoute,
    private userService: UserService,
    private router: Router) { }

  ngOnInit() {
    this.routeSub = this.route.params.subscribe(params => {
      console.log(params) //log the entire params object
      console.log(params['id']) //log the value of id
      this.userId = params['id'];
      this.userService.getUserByUserId(this.userId)
        .subscribe(
          data => {
            console.log(data)
            this.currentUserName = data.userDetails.userName
            this.userEmail = data.userDetails.userEmail
            console.log(this.currentUserName)
          }
        )

      this.userService.getAllUserFileDataByUserId(this.userId)
          .subscribe(data => {
            console.log(data);
            this.fileDatas = data.userDetails;
          })
    });
  }


 updateFile(fid, fileStatus){

  let reqStatus;
  if(fileStatus == "block"){
    reqStatus = "unblock";
  }
  else{
    reqStatus = "block";
  }

  Swal.fire({
    title : 'Type your request reason here to the admin..',
    input: 'text',
    inputPlaceholder: 'Type your message here..',
  }).then( data => {
    let responseData = {
      "userId" : Number(this.userId),
      "fileId": fid,
      "requestStatus": reqStatus,
      "requestMessage": data.value
    }
    console.log(responseData);
    this.userService.addFileRequestToAdmin(responseData)
      .subscribe(data =>{
        if(data.status == "success"){
          Swal.fire('Request Sent Suuccessfully');
        }
        else{
          Swal.fire('Error in sending request');
        }
      })
  })

 }

 downloadFile(fid){
  
    let data = {
      "id": this.userEmail,
      "fileId": fid,
    }
    console.log(data);
    this.userService.downloadFile(data).subscribe(data => {
      console.log(data);
    });

 }

 addFile(){

    Swal.fire({
    title: 'Upload Files',
    input: 'file',
    inputAttributes: {
      'accept': 'image/*,application/pdf,application/vnd.ms-powerpoint,application/msword',
      'multiple': 'multiple', 
      'aria-label': 'Upload your file'
    }
  }).then((file) => {
          console.log(file.value);
          console.log(file.value.length);
          let obj = {
            "userId": 1,
            "fileData": file
          }
          this.userService.uploadfile(obj)
            .subscribe(data => {
              console.log(data);
            })
          console.log(obj);
    }
  )

 }

 deleteFile(fid){
  console.log("File deleted with id:" + fid);
  let data = {
    "fileId": fid
  }

  this.userService.deleteUserFile(data)
    .subscribe(data => {
      if(data.status == "success"){
        Swal.fire("File Deleted Successfully");
        this.ngOnInit();
      }
      else{
        Swal.fire("Failed to Delete File. Please try again later")
      }
    })
 }

  BackButton(){
    this.router.navigate(['login'])
  }
}

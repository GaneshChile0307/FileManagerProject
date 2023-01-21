import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AlertService, AuthenticationService, UserService } from '../_services';
import Swal from 'sweetalert2';

@Component({templateUrl: 'login.component.html'})
export class LoginComponent implements OnInit {

    @ViewChild('email') emailElement: ElementRef;
    @ViewChild('password') passwordElement: ElementRef;
    loginForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
    id: string = '-1';
    email;
    password;
    

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService,
        private alertService: AlertService,
        emailElement: ElementRef,
        passwordElement: ElementRef) {
            this.emailElement = emailElement;
            this.passwordElement = passwordElement;
        }
        

    ngOnInit() {

        // reset login status
        this.authenticationService.logout();

        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    onRegister(){
        this.router.navigate(['/register']);
    }

    onGuest(){
        this.router.navigate(['/guest']);
    }
    

    onSubmit() {

        // console.log(this.emailElement.nativeElement.value + " " +this.passwordElement.nativeElement.value);

        let user = {
            "username": this.emailElement.nativeElement.value,
            "password": this.passwordElement.nativeElement.value
        }

        console.log(user);

        this.userService.loginUser(user)
            .subscribe(
                data => {
                    console.log(data);
                    // this.router.navigate(['/user/1'])

                    if(data.status == "success"){
                        if(data.userdetails.role == 1){
                            this.router.navigate(['/admin/'+data.userdetails.userID]);
                        }
                        
                        if(data.userdetails.role == 0){
                            this.router.navigate(['/user/'+data.userdetails.userID]);
                        }
                    }
                    else{
                        Swal.fire('User does not exist. Please register first!');
                        this.router.navigate(['/register']);
                    }    
                }
            );
    }
}

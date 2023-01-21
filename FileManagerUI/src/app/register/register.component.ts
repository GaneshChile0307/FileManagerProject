import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AlertService, UserService } from '../_services';
import { e } from '@angular/core/src/render3';
import Swal from 'sweetalert2';

@Component({templateUrl: 'register.component.html'})
export class RegisterComponent implements OnInit {
    @ViewChild('username') usernameElement: ElementRef;
    @ViewChild('password') passwordElement: ElementRef;
    @ViewChild('name') nameElement: ElementRef;    
    registerForm: FormGroup;
    loading = false;
    submitted = false;

    constructor(
        private formBuilder: FormBuilder,
        private router: Router,
        private userService: UserService,
        private alertService: AlertService,
        usernameElement: ElementRef,
        passwordElement: ElementRef,
        nameElement: ElementRef) {
            this.usernameElement = usernameElement;
            this.passwordElement = passwordElement;
            this.nameElement = nameElement;
         }

    ngOnInit() {

    }

    onBack(){
        this.router.navigate(['/login']);
    }

    onSubmit() {

       let user = {
        "username": this.usernameElement.nativeElement.value,
        "password": this.passwordElement.nativeElement.value,
        "name": this.nameElement.nativeElement.value 
        }
        console.log(user)

        this.userService.registerUser(user)
                .pipe(first())
                .subscribe(
                    data => {
                        console.log(data)
                        if(data.status == 'success'){
                            console.log("User Registration Successful!!");
                            Swal.fire('User Registration Successful!');
                            this.router.navigate(['/login']);
                        }
                        else{
                            console.log("User Registration Failed. Please try again.")
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'User already exists! Please try again with new email id!'
                              })
                            this.loading = false;

                        }
                        
                    },
                    error => {
                        this.alertService.error(error);
                        this.loading = false;
                    }
                    
                );
    
    }
}

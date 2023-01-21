import { Routes, RouterModule } from '@angular/router';
import { AdminComponent } from './admin/admin.component';
import { FileComponent } from './file/file.component';
import { GuestComponent } from './guest/guest.component';
import { HomeComponent } from './home';
import { LoginComponent } from './login';
import { RegisterComponent } from './register';
import { UserComponent } from './user/user.component';
import { AuthGuard } from './_guards';

const appRoutes: Routes = [
    { path: '', component: HomeComponent, canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    {path: 'user/:id', component: UserComponent},
    {path: 'admin/:id', component: AdminComponent},
    {path: 'guest', component: GuestComponent},
    {path: 'file/download/:id', component: FileComponent},
    // otherwise redirect to home
    { path: '**', redirectTo: '' }
];

export const routing = RouterModule.forRoot(appRoutes);
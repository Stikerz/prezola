import { Component, OnInit } from '@angular/core';
import {UserService} from '../../services/user.service';
import {ToastrService} from 'ngx-toastr';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  providers: []
})
export class RegisterComponent implements OnInit {

  username = '';
  firstname = '';
  lastname = '';
  password = '';



  constructor(private userService: UserService, private toastr: ToastrService) {}

    register() {
    if (!this.username || !this.firstname || !this.lastname || !this.password) {
      this.toastr.error('Error, please enter all fields correctly', 'Error');
    } else {
      this.userService.register({
        username: this.username,
        first_name: this.firstname, last_name: this.lastname,
        password: this.password
      });
    }
  }

  ngOnInit(): void {
  }

}


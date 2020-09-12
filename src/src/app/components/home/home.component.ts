import {Component, OnInit} from '@angular/core';
import {UserService} from '../../services/user.service';
import {Router} from '@angular/router';
import {WeddingService} from '../../services/wedding.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  token: string;
  gifts: any;

  constructor(private userService: UserService, private router: Router,
              private weddingService: WeddingService) {
  }

    ngOnInit(): void {
    this.userService.sharedToken.subscribe(data => this.token = data);
    if (this.token) {
      this.weddingService.getlist();
      this.weddingService.sharedWeddinglist.subscribe(data => this.gifts = data);
    } else {
      this.router.navigate(['login']);
    }

  }
    notPurchased(quantity: any, purchased: any ) {
    return quantity - purchased;
  }

}

import {Component, OnInit} from '@angular/core';
import {UserService} from '../../services/user.service';
import {Router} from '@angular/router';
import {WeddingService} from '../../services/wedding.service';

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.css']
})
export class ProductsComponent implements OnInit {
  token: string;
  products: any;

  constructor(private userService: UserService, private router: Router,
              private weddingService: WeddingService) {
  }

  ngOnInit(): void {
    this.userService.sharedToken.subscribe(data => this.token = data);
    if (this.token) {
      this.weddingService.getProducts();
      this.weddingService.sharedProducts.subscribe(data => this.products = data);
    } else {
      this.router.navigate(['login']);
    }

  }

}

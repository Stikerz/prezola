import { Component, OnInit } from '@angular/core';
import {UserService} from '../../services/user.service';
import {ActivatedRoute, Router} from '@angular/router';
import {WeddingService} from '../../services/wedding.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {
  token: string;
  product: any;
  idParam = '';
  constructor(private userService: UserService, private router: Router,
              private weddingService: WeddingService,
              private activateRoute: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.userService.sharedToken.subscribe(data => this.token = data);
    if (this.token) {
      this.activateRoute.params.subscribe(params => {
      this.idParam = params.id;
    });
      this.weddingService.getProduct(this.idParam);
      this.weddingService.sharedProduct.subscribe(data => this.product = data);
    } else {
      this.router.navigate(['login']);
    }

  }
  add() {
    this.weddingService.addList(this.idParam);
  }
  purchase() {
    this.weddingService.purchaseList(this.idParam);
  }
  delete() {
    this.weddingService.deleteList(this.idParam);
  }

}

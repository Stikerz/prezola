import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Router} from '@angular/router';
import {UserService} from './user.service';
import {BehaviorSubject} from 'rxjs';
import {ToastrService} from 'ngx-toastr';

@Injectable({
  providedIn: 'root'
})
export class WeddingService {
  baseUrl = 'http://127.0.0.1:8000';
  token: string;
  products: any = new BehaviorSubject([]);
  sharedProducts = this.products.asObservable();
  product: any = new BehaviorSubject({});
  sharedProduct = this.product.asObservable();
  weddinglist: any = new BehaviorSubject([]);
  sharedWeddinglist = this.weddinglist.asObservable();
  listDetail: any = [];
  errors: any = [];


  private httpOptionsToken: any;
  private httpOptionsMulti: any;

  constructor(private http: HttpClient, private router: Router, private userService: UserService, private toastr: ToastrService) {
    this.userService.sharedToken.subscribe(data => this.token = data);
    this.httpOptionsToken = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: 'Token ' + this.token
      })
    };

    this.httpOptionsMulti = {
      headers: new HttpHeaders({
        Authorization: 'Token ' + this.token
      })
    };
  }

  updateHeader() {
    this.httpOptionsToken = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: 'Token ' + this.token
      })
    };
    this.httpOptionsMulti = {
      headers: new HttpHeaders({
        Authorization: 'Token ' + this.token
      })
    };
  }

  public getProducts() {
    this.updateHeader();
    this.http.get(this.baseUrl + '/weddingshop/products', this.httpOptionsToken).subscribe(
      data => {
        this.products.next(data);
      },
      err => {
        console.log(this.httpOptionsToken);
        this.toastr.error('Error Retrieving Products', 'Error');
        this.errors = err.error;
      }
    );
  }

  public getProduct(id) {
    this.updateHeader();
    this.http.get(this.baseUrl + '/weddingshop/product/' + id, this.httpOptionsToken).subscribe(
      data => {
        this.product.next(data);
      },
      err => {
        this.toastr.error('Error Retrieving Product', 'Error');
        this.errors = err.error;
      }
    );
  }

  public getlist() {
    this.updateHeader();
    this.http.get(this.baseUrl + '/weddingshop/list', this.httpOptionsToken).subscribe(
      data => {
        this.weddinglist.next(data);
      },
      err => {
        console.log(this.httpOptionsToken);
        this.toastr.error('Error Retrieving Weddinglist', 'Error');
        this.errors = err.error;
      }
    );
  }

  public getlistDetail(id) {
    this.updateHeader();
    this.http.get(this.baseUrl + '/weddingshop/list?search=' + id, this.httpOptionsToken).subscribe(
      data => {
        this.listDetail = data;
      },
      err => {
        console.log(this.httpOptionsToken);
        this.toastr.error('Error Retrieving Weddinglist Detail', 'Error');
        this.errors = err.error;
      }
    );
  }

  public addList(id) {
    this.getlistDetail(id);
    setTimeout(() => {
        if (this.listDetail.length > 0) {
          const data1 = {
            product: this.listDetail[0].product,
            quantity: this.listDetail[0].quantity + 1,
            purchased: this.listDetail[0].purchased
          };
          this.http.put(this.baseUrl + '/weddingshop/listitem/' + this.listDetail[0].id + '/', data1, this.httpOptionsMulti).subscribe(
            data2 => {
              this.toastr.success('Updated List');
            },
            err => {
              this.toastr.error('Error updating to List', 'Error');
              console.log(err.error);
              this.errors = err.error;
            }
          );

        } else {
          const data1 = {product: id, quantity: 1, purchased: 0};
          this.updateHeader();
          this.http.post(this.baseUrl + '/weddingshop/list/', data1, this.httpOptionsMulti).subscribe(
            data2 => {
              this.toastr.success('Added to List');
            },
            err => {
              this.toastr.error('Error Adding to List', 'Error');
              console.log(err.error);
              this.errors = err.error;
            }
          );

        }
        // this.getlist();


      }


      , 1000);
  }
    public purchaseList(id) {
    this.getlistDetail(id);
    setTimeout(() => {
        if (this.listDetail.length > 0 && this.listDetail[0].quantity > 0) {
          console.log(this.listDetail);
          const data1 = {
            product: this.listDetail[0].product,
            quantity: this.listDetail[0].quantity ,
            purchased: this.listDetail[0].purchased + 1
          };
          this.http.put(this.baseUrl + '/weddingshop/listitem/' + this.listDetail[0].id + '/', data1, this.httpOptionsMulti).subscribe(
            data2 => {
              this.toastr.success('Updated List');
            },
            err => {
              this.toastr.error('Error updating to List', 'Error');
              console.log(err.error);
              this.errors = err.error;
            }
          );

        } else {
            this.toastr.error('Please add gift to list before purchase', 'Error');
        }
        this.getProduct(id);
      }


      , 1000);
  }
    public deleteList(id) {
    this.getlistDetail(id);
    setTimeout(() => {
          this.http.delete(this.baseUrl + '/weddingshop/listitem/' +  this.listDetail[0].id + '/', this.httpOptionsToken).subscribe(
      data => {
        this.toastr.success('Removed gift from List');
        this.router.navigate(['']);

      },
      err => {
        this.toastr.error('Error Deleting gift', 'Error');
        this.errors = err.error;
      }
    );
    } , 1000 );
      }
  }







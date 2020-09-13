import {Component, OnInit, ViewChild, ElementRef} from '@angular/core';
import {UserService} from '../../services/user.service';
import {Router} from '@angular/router';
import {WeddingService} from '../../services/wedding.service';
import { jsPDF } from "jspdf";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  token: string;
  gifts: any;

    @ViewChild('weddingtable') weddingtable: ElementRef;

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
    public openPDF(): void {
    const DATA = this.weddingtable.nativeElement;
    // @ts-ignore
    const doc = new jsPDF('p', 'pt', 'a4');
    console.log(doc);
    doc.html(DATA.innerHTML, {
        // tslint:disable-next-line:no-shadowed-variable
        callback(doc) {
          doc.save();
        },
        x: 15,
        y: 15
      });
  }

}

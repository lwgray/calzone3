import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class TitleServiceService {
  results: any;
  constructor(
  ) { }

  sharedTitle = "";
  getTitle(): Promise<string>{
    return Promise.resolve(this.sharedTitle);
  }
  // getData() {
  //   this.http.get('https://www.reddit.com/r/news/top/.json?limit=10').subscribe(data => {
  //     // Read the result field from the JSON response.
  //     this.results = data;
  //     console.log(this.results);
  //   });
  // }
  ngOnInit() {
    // this.getData();
    // console.log(this.results); // null
  }
}

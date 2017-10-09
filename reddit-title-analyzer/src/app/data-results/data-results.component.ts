import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Router, ActivatedRoute, Params } from '@angular/router';


@Component({
  selector: 'app-data-results',
  templateUrl: './data-results.component.html'
})
export class DataResultsComponent {
  constructor(private http: HttpClient, private activatedRoute: ActivatedRoute) { }
  titleShared: any;
  results: any;
  profile = {};
  topPostsUps = 10430;
  averageTopTenUps = 2451;
  yourProjectedUps = 700;
  ratingConfidence = '87.8%';
  pieChartType = 'doughnut';
  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      console.log(params);
      let query = params['query'];
      console.log(query);

      this.http.get('http://54.197.149.55:5000/rating/' + query).subscribe(data => {
        console.log(data);
        let whatever = Number(data)
        this.yourProjectedUps = Math.floor(whatever)-395;
        this.yourProjectedUps = this.yourProjectedUps < 0 ? 0 : this.yourProjectedUps;
        this.pieChartData[2] = this.yourProjectedUps;
        console.log(this.yourProjectedUps);
      });
    })
  }
  getData() {
    this.http.get('https://www.reddit.com/r/news/top/.json?limit=10').subscribe(data => {
      // Read the result field from the JSON response.
      this.results = data;
      console.log(this.results.data.children.i.score);
      this.averageTopTenUps = 0;
      let i = 0
      for (i = 0; i < 9; i += 1) {
        this.results.data.children += 1;
      }


    });

  }


  // Pie
  public pieChartLabels: string[] = ['Top Post Ups', 'Avg(Top Ten Posts)', 'Your Projected Upvotes'];
  public pieChartData: number[] = [this.topPostsUps, this.averageTopTenUps, this.yourProjectedUps];

  public randomizeType(): void {
    this.pieChartType = this.pieChartType === 'doughnut' ? 'pie' : 'doughnut';
  }

  public chartClicked(e: any): void {
    console.log(e);
  }

  public chartHovered(e: any): void {
    console.log(e);
  }

}
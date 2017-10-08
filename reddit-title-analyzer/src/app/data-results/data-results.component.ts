import { Component } from '@angular/core';

@Component({
  selector: 'app-data-results',
  templateUrl: './data-results.component.html'
})
export class DataResultsComponent {
  topPostsUps = 10430;
  averageTopTenUps = 2451;
  yourProjectedUps = 738;
  ratingConfidence = '87.8%';
  pieChartType = 'doughnut';
 
  // Pie
  public pieChartLabels:string[] = ['Top Post Ups', 'Avg(Top Ten Posts)', 'Your Projected Upvotes'];
  public pieChartData:number[] = [this.topPostsUps, this.averageTopTenUps, this.yourProjectedUps];
 
  public randomizeType():void {
    this.pieChartType = this.pieChartType === 'doughnut' ? 'pie' : 'doughnut';
  }
 
  public chartClicked(e:any):void {
    console.log(e);
  }
 
  public chartHovered(e:any):void {
    console.log(e);
  }
}
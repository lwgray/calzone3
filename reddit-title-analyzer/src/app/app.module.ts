import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import 'rxjs/add/operator/map'
import { AppComponent } from './app.component';
import { MatInputModule, MatCardModule, MatButtonModule, MatAutocompleteModule, MatIconModule, MatToolbarModule } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { FormsModule, ReactiveFormsModule, FormControl } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { StartPageComponent } from './start-page/start-page.component';
import { DataResultsComponent } from './data-results/data-results.component';
import { ChartsModule } from 'ng2-charts';
const appRoutes: Routes = [
  { path: 'start', component: StartPageComponent },
  { path: 'results', component: DataResultsComponent },
  // { path: '**', component: StartPageComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    StartPageComponent,
    DataResultsComponent
  ],
  imports: [
    ChartsModule,
    RouterModule.forRoot(appRoutes),
    ReactiveFormsModule,
    FormsModule,
    MatInputModule,
    BrowserModule,
    MatCardModule,
    MatButtonModule,
    MatAutocompleteModule,
    FlexLayoutModule,
    MatIconModule,
    MatToolbarModule,
    BrowserAnimationsModule],
  providers: [StartPageComponent,
    DataResultsComponent,
    FormsModule],
  bootstrap: [AppComponent]
})
export class AppModule { }

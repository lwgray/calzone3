import { BrowserModule } from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import 'rxjs/add/operator/map'
import { AppComponent } from './app.component';
import { MatInputModule,MatCardModule, MatButtonModule, MatAutocompleteModule, MatIconModule, MatToolbarModule } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { FormsModule, ReactiveFormsModule, FormControl} from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent
  ],
  imports: [
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
    BrowserAnimationsModule  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

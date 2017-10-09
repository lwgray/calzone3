import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DataResultsComponent } from './data-results.component';
import {Router, ActivatedRoute, Params} from '@angular/router';

describe('DataResultsComponent', () => {
  let component: DataResultsComponent;
  let fixture: ComponentFixture<DataResultsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DataResultsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DataResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

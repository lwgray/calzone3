import { TestBed, inject } from '@angular/core/testing';

import { TitleServiceService } from './title-service.service';

describe('TitleServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TitleServiceService]
    });
  });

  it('should be created', inject([TitleServiceService], (service: TitleServiceService) => {
    expect(service).toBeTruthy();
  }));
});

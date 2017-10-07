import { UmbcHackathonPage } from './app.po';

describe('umbc-hackathon App', () => {
  let page: UmbcHackathonPage;

  beforeEach(() => {
    page = new UmbcHackathonPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});

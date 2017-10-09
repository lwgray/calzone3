import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { FormControl } from '@angular/forms';
import {Router, ActivatedRoute, Params} from '@angular/router';

@Component({
  selector: 'app-start-page',
  templateUrl: './start-page.component.html',
  styleUrls: ['./start-page.component.css']
})
export class StartPageComponent implements OnInit {

  ngOnInit() {
    
  }
  mySubreddit = ""
  titletext = "";
  filteredStates: Observable<any[]>;
  stateCtrl: FormControl;
  
  states: any[] = [
    { rank: '1', name: '/r/announcements', subscribers: '19326510' },
    { rank: '2', name: '/r/funny', subscribers: '18140816' },
    { rank: '3', name: '/r/AskReddit', subscribers: '17994504' },
    { rank: '4', name: '/r/todayilearned', subscribers: '17819928' },
    { rank: '5', name: '/r/science', subscribers: '17747966' },
    { rank: '6', name: '/r/worldnews', subscribers: '17688376' },
    { rank: '7', name: '/r/pics', subscribers: '17674462' },
    { rank: '8', name: '/r/IAmA', subscribers: '17326862' },
    { rank: '9', name: '/r/gaming', subscribers: '17025916' },
    { rank: '10', name: '/r/videos', subscribers: '16894463' },
    { rank: '11', name: '/r/movies', subscribers: '16612503' },
    { rank: '12', name: '/r/aww', subscribers: '16072715' },
    { rank: '13', name: '/r/blog', subscribers: '16040701' },
    { rank: '14', name: '/r/Music', subscribers: '16002253' },
    { rank: '15', name: '/r/gifs', subscribers: '15218651' },
    { rank: '16', name: '/r/news', subscribers: '15155828' },
    { rank: '17', name: '/r/explainlikeimfive', subscribers: '14801174' },
    { rank: '18', name: '/r/askscience', subscribers: '14714407' },
    { rank: '19', name: '/r/EarthPorn', subscribers: '14335255' },
    { rank: '20', name: '/r/books', subscribers: '13815779' },
    { rank: '21', name: '/r/television', subscribers: '13747462' },
    { rank: '22', name: '/r/LifeProTips', subscribers: '13338248' },
    { rank: '23', name: '/r/mildlyinteresting', subscribers: '13339159' },
    { rank: '24', name: '/r/space', subscribers: '13054709' },
    { rank: '25', name: '/r/Showerthoughts', subscribers: '12961667' },
    { rank: '26', name: '/r/DIY', subscribers: '12875176' },
    { rank: '27', name: '/r/Jokes', subscribers: '12745930' },
    { rank: '28', name: '/r/sports', subscribers: '12666210' },
    { rank: '29', name: '/r/gadgets', subscribers: '12654624' },
    { rank: '30', name: '/r/tifu', subscribers: '12624528' },
    { rank: '31', name: '/r/nottheonion', subscribers: '12595094' },
    { rank: '32', name: '/r/InternetIsBeautiful', subscribers: '12539917' },
    { rank: '33', name: '/r/photoshopbattles', subscribers: '12484713' },
    { rank: '34', name: '/r/food', subscribers: '12475172' },
    { rank: '35', name: '/r/history', subscribers: '12463360' },
    { rank: '36', name: '/r/Futurology', subscribers: '12444465' },
    { rank: '37', name: '/r/Documentaries', subscribers: '12415646' },
    { rank: '38', name: '/r/dataisbeautiful', subscribers: '12413537' },
    { rank: '39', name: '/r/listentothis', subscribers: '12364625' },
    { rank: '40', name: '/r/UpliftingNews', subscribers: '12333864' },
    { rank: '41', name: '/r/personalfinance', subscribers: '12321831' },
    { rank: '42', name: '/r/GetMotivated', subscribers: '12249798' },
    { rank: '43', name: '/r/OldSchoolCool', subscribers: '12198070' },
    { rank: '44', name: '/r/philosophy', subscribers: '12188081' },
    { rank: '45', name: '/r/Art', subscribers: '11991037' },
    { rank: '46', name: '/r/nosleep', subscribers: '11768049' },
    { rank: '47', name: '/r/creepy', subscribers: '11752819' },
    { rank: '48', name: '/r/WritingPrompts', subscribers: '11713129' },
    { rank: '49', name: '/r/TwoXChromosomes', subscribers: '11292716' },
    { rank: '50', name: '/r/Fitness', subscribers: '6202593' },
    { rank: '51', name: '/r/technology', subscribers: '5619591' },
    { rank: '52', name: '/r/WTF', subscribers: '4894902' },
    { rank: '53', name: '/r/bestof', subscribers: '4791143' },
    { rank: '54', name: '/r/AdviceAnimals', subscribers: '4353662' },
    { rank: '55', name: '/r/politics', subscribers: '3504317' },
    { rank: '56', name: '/r/atheism', subscribers: '2108648' },
    { rank: '57', name: '/r/europe', subscribers: '1552657' },
    { rank: '58', name: '/r/interestingasfuck', subscribers: '1491976' },
    { rank: '59', name: '/r/woahdude', subscribers: '1405175' },
    { rank: '61', name: '/r/gameofthrones', subscribers: '1158131' },
    { rank: '62', name: '/r/leagueoflegends', subscribers: '1155123' },
    { rank: '63', name: '/r/pcmasterrace', subscribers: '1149458' },
    { rank: '64', name: '/r/BlackPeopleTwitter', subscribers: '1136587' },
    { rank: '65', name: '/r/reactiongifs', subscribers: '1105460' },
    { rank: '66', name: '/r/trees', subscribers: '1024488' },
    { rank: '67', name: '/r/Unexpected', subscribers: '1016157' },
    { rank: '68', name: '/r/oddlysatisfying', subscribers: '988824' },
    { rank: '69', name: '/r/Overwatch', subscribers: '974897' },
    { rank: '70', name: '/r/Android', subscribers: '929936' },
    { rank: '71', name: '/r/wholesomememes', subscribers: '923269' },
    { rank: '72', name: '/r/programming', subscribers: '853920' },
    { rank: '73', name: '/r/Games', subscribers: '850371' },
    { rank: '74', name: '/r/facepalm', subscribers: '846921' },
    { rank: '75', name: '/r/nba', subscribers: '838407' },
    { rank: '77', name: '/r/4chan', subscribers: '831148' },
    { rank: '78', name: '/r/me_irl', subscribers: '817456' },
    { rank: '79', name: '/r/relationships', subscribers: '816639' },
    { rank: '80', name: '/r/lifehacks', subscribers: '812602' },
    { rank: '81', name: '/r/cringepics', subscribers: '809858' },
    { rank: '82', name: '/r/fffffffuuuuuuuuuuuu', subscribers: '782762' },
    { rank: '83', name: '/r/sex', subscribers: '780465' },
    { rank: '84', name: '/r/pokemon', subscribers: '777673' },
    { rank: '85', name: '/r/tattoos', subscribers: '776640' },
    { rank: '86', name: '/r/comics', subscribers: '763889' },
    { rank: '87', name: '/r/soccer', subscribers: '760010' },
    { rank: '88', name: '/r/reddit.com', subscribers: '758224' },
    { rank: '89', name: '/r/Frugal', subscribers: '757143' },
    { rank: '91', name: '/r/pokemongo', subscribers: '738192' },
    { rank: '93', name: '/r/ImGoingToHellForThis', subscribers: '722079' },
    { rank: '94', name: '/r/CrappyDesign', subscribers: '722469' },
    { rank: '95', name: '/r/malefashionadvice', subscribers: '707795' },
    { rank: '96', name: '/r/OutOfTheLoop', subscribers: '705854' },
    { rank: '97', name: '/r/StarWars', subscribers: '675050' },
    { rank: '98', name: '/r/dankmemes', subscribers: '676991' },
    { rank: '99', name: '/r/buildapc', subscribers: '669663' },
    { rank: '100', name: '/r/YouShouldKnow', subscribers: '663597' }
  ];

  constructor(private activatedRoute: ActivatedRoute) {
    
    this.stateCtrl = new FormControl();
    this.filteredStates = this.stateCtrl.valueChanges
        .startWith(null)
        .map(state => state ? this.filterStates(state) : this.states.slice());
    
  }

  filterStates(name: string) {
    return this.states.filter(state =>
      state.name.slice(3).toLowerCase().indexOf(name.toLowerCase()) === 0);
  }


}

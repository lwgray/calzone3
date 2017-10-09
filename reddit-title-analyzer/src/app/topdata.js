var express = require('express')
var app = express()

let dataj = app.get('https://www.reddit.com/r/news/top/.json?limit=10', function(req, res) {
    console.log(res.body);
  });

  console.log(dataj)
module.export = dataj;

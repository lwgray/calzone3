const reddit = require('./reddit_config');
const Promise = require('bluebird');

var parseAsync = Promise.method(JSON.parse);

reddit.getSubreddit('nfl').getHot({limit: 100}).map(post => post.upvote()).then(console.log)





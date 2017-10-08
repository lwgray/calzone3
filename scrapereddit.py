import praw
import json
import yaml
import jsonpickle
i = 0
filename = "testfile.json"
reddit = praw.Reddit(client_id='kZLtaDQZnQAcrw',
                    client_secret='cJhtGj9LEdBj5PK6AnMRQLgb7xQ',
                    password='vasanth9876',
                    user_agent='RedditApiClient/0.1 by Vasanth',
                    username='vk432')
reddit.config.log_requests=1
reddit.config.store_json_result = True
subreddit = reddit.subreddit('politics')
list_of_submissions = []
for submission in subreddit.submissions(1496361328, 1507334128):
   i += 1
   if i % 50 == 0:
      print i
   if submission.over_18 == False:
      list_of_submissions.append({"subreddit": submission.subreddit.title ,"ups": submission.ups, "title":submission.title})


with open(filename, 'w') as json_file:
      json.dump(list_of_submissions, json_file)
# for submission in reddit.subreddit('sports').top(limit=2000):
   # i +=1
   # print i
   # print(submission.title.encode("utf-8"))
   
# json_str = json.dumps(list_of_items)


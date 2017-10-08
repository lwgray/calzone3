import praw
import json
import sqlite3 as lite
import sys
import string

reddit = praw.Reddit(client_id='kZLtaDQZnQAcrw',
                    client_secret='cJhtGj9LEdBj5PK6AnMRQLgb7xQ',
                    password='vasanth9876',
                    user_agent='RedditApiClient/0.1 by Vasanth',
                    username='vk432')

subreddit = reddit.subreddit('politics')
list_of_submissions = subreddit.submissions(1504657288, 1507249288)

con = None
i=0
try:
    con = lite.connect('redditposts.db')
    con.text_factory = str
    with con:
       cur = con.cursor()  
       for submission in list_of_submissions:
          i+=1
          if i % 50 == 0:
             print i
         

          # print command
          cur.execute ("""
             INSERT INTO posts 
             VALUES(null,?,?,?)
            """,
            (submission.title.encode("utf-8"),submission.ups,"Politics")
          )
            
except lite.Error, e:
    print e
    pass
    
finally:
    
    if con:
        con.close()
import calendar
from datetime import datetime
import pandas as pd
import csv
import praw
from configparser import ConfigParser
import time


config = ConfigParser()
config.read('../config2.ini')

reddit = praw.Reddit(
    # [client_data]
    client_id=config["client_data"]["client_id"],
    client_secret=config["client_data"]["client_secret"],
    user_agent=config["client_data"]["user_agent"],

    # [credentials]
    username=config["credentials"]["username"],
    password=config["credentials"]["password"]
)


def get_timestamps(time1, time2):
    month1, day1, year1 = time1.split('/')
    month2, day2, year2 = time2.split('/')
    dt1 = datetime(int(year1), int(month1), int(day1))
    dt2 = datetime(int(year2), int(month2), int(day2))
    t1 = calendar.timegm(dt1.timetuple())
    t2 = calendar.timegm(dt2.timetuple())
    return t1, t2


t1, t2 = get_timestamps('11/13/2017', '12/13/2017')
sbrt = pd.read_csv('subreddit.csv')
s = sbrt.subreddit.tolist()

'''
with open('posts.csv', 'a') as posts:
    writer = csv.writer(posts)
    for subreddit in s:
        x = reddit.subreddit(subreddit)
        submissions = x.submissions(t1, t2)
        for index, data in enumerate(submissions):
            try:
                print (subreddit, index, data.title)
                if index > 2000:
                    break
                writer.writerow([data.id, data.subreddit_name_prefixed, data.title,
                                data.ups, data.url, str(data.created_utc)])
            except:
                time.sleep(3600)
                continue
'''

with open('posts.csv', 'a') as posts:
    writer = csv.writer(posts)
    for subreddit in s:
        index = 0
        x = reddit.subreddit(subreddit)
        submissions = x.submissions(t1, t2)
        while index <= 2000:
            try:
                data = next(submissions)
                print (subreddit, index, data.title)
                writer.writerow([data.id, data.subreddit_name_prefixed, data.title,
                                data.ups, data.url, str(data.created_utc)])
                index += 1
            except StopIteration:
                break
            except:
                for i in xrange(3600,0,-1):
                    time.sleep(1)
                    print(i)
                continue


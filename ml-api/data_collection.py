from datetime import datetime
import calendar
import praw
import pandas as pd
from config import ConfigParser

config = ConfigParser('../config_data_collection.ini')


# To specifying date ranges in PRAW require timestamps
def get_timestamps(time1, time2):
    ''' Convert date range into timestamps
    
    time1(str):  start date formated as 01/01/2001
    time2(str):  end date formated as 01/01/2001
    
    returns(str) start and end timestamps
    '''
    month1, day1, year1 = time1.split('/')
    month2, day2, year2 = time2.split('/')
    dt1 = datetime(int(year1), int(month1), int(day1))
    dt2 = datetime(int(year2), int(month2), int(day2))
    t1 = calendar.timegm(dt1.timetuple())
    t2 = calendar.timegm(dt2.timetuple())
    return t1, t2


# Step 1: Intialize reddit connection
reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                     password=config.password, user_agent=config.useragent,
                     username=config.username)
# Step 2: define subreddit to capture
subreddit = reddit.subreddit('politics')


# Step 3: Select time frame and acquire posts from specified subreddit
t1, t2 = get_timestamps('01/01/2017', '12/31/2017')
submissions = subreddit.submissions(t1, t2)

# Step 4: Extract pertinent information from posts
data = [[data.id, data.subreddit_name_prefixed,
         data.title, data.ups, data.url,
         data.created_utc] for data in submissions]

# Step 5: Place data in pandas dataframe
df = pd.DataFrame(data, columns=['id', 'subreddit', 'title',
                                 'ups', 'url', 'created_utc'])
# Step 6: Save to CSV file
df.to_csv('data_blog.csv', index=False)

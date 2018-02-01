""" Script to Search for posts within Subreddits """
import calendar
from datetime import datetime
import time
import argparse
import sys
import pandas as pd
import praw
from configparser import ConfigParser
from pp_test import process


CONFIG = ConfigParser()
CONFIG.read('../config2.ini')

REDDIT = praw.Reddit(
    # [client_data]
    client_id=CONFIG["client_data"]["client_id"],
    client_secret=CONFIG["client_data"]["client_secret"],
    user_agent=CONFIG["client_data"]["user_agent"],

    # [credentials]
    username=CONFIG["credentials"]["username"],
    password=CONFIG["credentials"]["password"]
)


def get_timestamps(time1, time2):
    """Convert Dates to Timestamps

    Args:
        time1(str): Start time in '01/01/2001' format
        time2(str): End Time in '01/01/2001' format

    Returns:
        t1(float): Timestamp for start date
        t2(float): Timestamp for end date

    """
    month1, day1, year1 = time1.split('/')
    month2, day2, year2 = time2.split('/')
    dt1 = datetime(int(year1), int(month1), int(day1))
    dt2 = datetime(int(year2), int(month2), int(day2))
    timestamp1 = calendar.timegm(dt1.timetuple())
    timestamp2 = calendar.timegm(dt2.timetuple())
    return timestamp1, timestamp2


def grab_posts(sub=False, f_input='subreddit.csv', number=2000,
               f_output='posts.csv', start=None, end=None, verbose=False):
    """ Grab Subreddit posts under various conditions

    Args:
        sub(str): The name of subreddit to search
        f_input(str):       The file with a list of subreddits to search
        number(int):        The number of posts to retreive
        f_output(str):      The name of a file to write posts to
        start/end(str):     The date range to search
        verbose(boolean):   Print out information about subreddit

    Returns:
        data(Pandas Dataframe): DataFrame with retrieved posts

    """
    if sub:
        subs = [sub]
    else:
        sbrt = pd.read_csv(f_input)
        subs = sbrt.subreddit.tolist()

    for subreddit in subs:
        features = []
        index = 0
        post = REDDIT.subreddit(subreddit)
        if start is not None and end is not None:
            timestamp1, timestamp2 = get_timestamps(start, end)
            submissions = post.submissions(timestamp1, timestamp2)
        else:
            submissions = post.submissions()
        while index <= number:
            try:
                data = next(submissions)
                if verbose:
                    print (subreddit, index, data.title)
                features.append([data.id, data.subreddit_name_prefixed,
                                 data.title, data.ups,
                                 data.url, str(data.created_utc)])
                index += 1
                attempts = 1
            except StopIteration:
                break
            except Exception as msg:
                print('General Exception', str(msg), data.title)
                for i in range(60 * attempts, 0, -1):
                    time.sleep(1)
                    print(i)
                attempts += 1
                continue
        dframe = pd.DataFrame(data=features,
                              columns=['id', 'subreddit', 'title', 'ups',
                                       'url', 'created_utc'])
        data = process(dframe, 'processed_{0}.csv'.format(subreddit))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Grab posts by time')
    parser.add_argument('--subreddit', '-s', default=False,
                        help="Choose subreddit to search")
    parser.add_argument('--input', '-i', default='subreddit.csv',
                        help="CSV file containing list of subreddits")
    parser.add_argument('--output', '-o', default=False,
                        help="CSV file to write data to")
    parser.add_argument('--start', '-t1',
                        help="Start date - format month/day/year")
    parser.add_argument('--end', '-t2',
                        help="End date - format month/day/year")
    parser.add_argument('--number', '-n', default=2000, type=int,
                        help="The number of posts to grab")
    parser.add_argument('--verbose', '-v', default=False,
                        help="Turn on print-to-screen")
    args = parser.parse_args()
    sys.exit(grab_posts(args.subreddit, args.input, args.number, args.output,
                        args.start, args.end))

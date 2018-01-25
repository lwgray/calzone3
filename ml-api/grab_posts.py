import calendar
from datetime import datetime
import pandas as pd
import csv
import praw
from configparser import ConfigParser
import time
import argparse
import sys
from process_posts import process


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


def main(sub=False, f_input='subreddit.csv', number=2000, f_output='posts.csv', start=None, end=None):
    print(f_input)
    print(f_output)
    print(number)
    if sub:
        s = [sub]
    else:
        sbrt = pd.read_csv(f_input)
        s = sbrt.subreddit.tolist()
        print(s[:3])

    with open(f_output, 'a') as posts:
        writer = csv.writer(posts)
        for subreddit in s:
            index = 0
            x = reddit.subreddit(subreddit)
            if start is not None and end is not None:
                t1, t2 = get_timestamps(start, end)
                submissions = x.submissions(t1, t2)
            else:
                submissions = x.submissions()
            while index <= number:
                try:
                    data = next(submissions)
                    print (subreddit, index, data.title.encode("utf-8") )
                    writer.writerow([data.id, data.subreddit_name_prefixed,
                                     data.title.encode("utf-8"), data.ups, data.url,
                                     str(data.created_utc)])
                    index += 1
                except StopIteration:
                    break
                except Exception as e:
                    print('General Exception', str(e), data.title)
                    for i in range(3600, 0, -1):
                        time.sleep(1)
                        print(i)
                    continue
    process(f_output, 'processed_{0}'.format(f_output))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Grab posts by time')
    parser.add_argument('--subreddit', '-s', default='python',
                        help="Choose subreddit to search")
    parser.add_argument('--input', '-i', default='subreddit.csv',
                        help="Name of input file")
    parser.add_argument('--output', '-o', default='posts.csv',
                        help="Name of output file")
    parser.add_argument('--start', '-t1', help="Start date - format month/day/year")
    parser.add_argument('--end', '-t2', help="End date - format month/day/year")
    parser.add_argument('--number', '-n', default=2000, type=int, help="The number of posts to grab")
    args = parser.parse_args()
    sys.exit(main(args.subreddit, args.input, args.number, args.output,
                  args.start, args.end))

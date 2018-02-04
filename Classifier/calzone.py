""" Script to Search for posts within Subreddits """
import calendar
from datetime import datetime
import time
import argparse
import sys
import pandas as pd
import praw
from configparser import ConfigParser
# from process_posts import process
from feature_extraction import Blob
import numpy as np


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



def process(data, f_output):
    """Perform preprocessing on data. 
       1. Add headers
       2. Remove Duplicate titles
       3. Remove subreddits without readable titles
       4. Remove subreddit specific words from titles

    f_input csv: contains data downloaded from reddit
    f_output csv: file name to write processed data to

    """
    pd.set_option('display.float_format', lambda x: '%.1f' % x)

    # Remove Duplicate Titles
    data.drop_duplicates('title', inplace=True)

    # Remove unwanted subreddit
    data = data[data['subreddit'] != 'r/me_irl']

    # Remove repetitive words from subreddit titles
    # for instance 'TIL' from r/todayilearned subreddit
    if 'r/todayilearned' in data.subreddit.values:
        data.loc[data.subreddit == 'r/todayilearned',
                 'title'] = data.loc[data['subreddit'] == 'r/todayilearned',
                                     'title'].str.replace('TIL', '')

    if 'r/photoshopbattles' in data.subreddit.values:
        data.loc[data.subreddit == 'r/photoshopbattles',
                 'title'] = data.loc[data['subreddit'] == 'r/photoshopbattles',
                                     'title'].str.replace('PsBattle:', '')

    data.to_csv('{0}.bz2'.format(f_output), index=False,
                compression='bz2', encoding='utf-8')
    return data



def describe(data):
    """ Display Title Characteristics

    Args:
        data(DataFrame): Dataframe containing subreddit titles

    Returns:
        df(DataFrame): Dataframe containing several characteristics of title
	
	1.  Max length of title (characters)
	2.  Average Length of title (characters)
	3.  Max number of words in title (words)
	4.  Average number of words in title (words)
	5.  Average Sentiment Polarity
	6.  Average Sentiment Subjectivity
	7.  Average number of Noun Phrases
	
	These values are obtained for all titles,
	titles that have greater than average upvotes,
	and titles than have less than average upvotes
    """
    blob = Blob()

    all_blob = blob.transform(data.title)
    noun_phrases, subjectivity, polarity = zip(*all_blob)
    all_max_len_title = max([len(x) for x in data['title']])
    all_avg_len_title = int(np.mean([len(x) for x in data['title']]))
    all_max_word_count = max([len(x.split()) for x in data['title']])
    all_avg_word_count = int(np.mean([len(x.split()) for x in data['title']]))
    all_polarity = sum(polarity)/len(polarity)
    all_subjectivity = sum(subjectivity)/len(subjectivity)
    all_noun_phrases = sum(noun_phrases)/len(noun_phrases)
    all_votes = data.ups.mean()

    greater_than_avg = data['ups'] > data['ups'].mean()
    gt_avg_blob = blob.transform(data[greater_than_avg]['title'])
    noun_phrases, subjectivity, polarity = zip(*gt_avg_blob)
    gt_avg_max_len_title = max([len(x) for x in data[greater_than_avg]['title']])
    gt_avg_avg_len_title = int(np.mean([len(x) for x in data[greater_than_avg]['title']]))
    gt_avg_max_word_count = max([len(x.split()) for x in data[greater_than_avg]['title']])
    gt_avg_avg_word_count = int(np.mean([len(x.split()) for x in data[greater_than_avg]['title']]))
    gt_avg_polarity= sum(polarity)/len(polarity)
    gt_avg_subjectivity= sum(subjectivity)/len(subjectivity)
    gt_avg_noun_phrases= sum(noun_phrases)/len(noun_phrases)
    gt_avg_votes = data[greater_than_avg]['ups'].mean()

    less_than_avg = data['ups'] <= data['ups'].mean()
    lt_avg_blob = blob.transform(data[less_than_avg]['title'])
    noun_phrases, subjectivity, polarity = zip(*lt_avg_blob)
    lt_avg_max_len_title = max([len(x) for x in data[less_than_avg]['title']])
    lt_avg_avg_len_title = int(np.mean([len(x) for x in data[less_than_avg]['title']]))
    lt_avg_max_word_count = max([len(x.split()) for x in data[less_than_avg]['title']])
    lt_avg_avg_word_count = int(np.mean([len(x.split()) for x in data[less_than_avg]['title']]))
    lt_avg_polarity= sum(polarity)/len(polarity)
    lt_avg_subjectivity= sum(subjectivity)/len(subjectivity)
    lt_avg_noun_phrases= sum(noun_phrases)/len(noun_phrases)
    lt_avg_votes = data[less_than_avg]['ups'].mean()

    data = {'Max_Title': [all_max_len_title, gt_avg_max_len_title, lt_avg_max_len_title],
	    'Avg_Title': [all_avg_len_title, gt_avg_avg_len_title, lt_avg_avg_len_title],
            'Max_Word_Count': [all_max_word_count, gt_avg_max_word_count, lt_avg_max_word_count],
            'Avg_Word_Count': [all_avg_word_count, gt_avg_avg_word_count, lt_avg_avg_word_count],
	    'Noun_Phrases':[all_noun_phrases, gt_avg_noun_phrases, lt_avg_noun_phrases],
	    'Subjectivity':[all_subjectivity, gt_avg_subjectivity, lt_avg_subjectivity],
	    'Polarity':[all_polarity, gt_avg_polarity, lt_avg_polarity],
	    'Avg_Votes':[all_votes, gt_avg_votes, lt_avg_votes]}
    df = pd.DataFrame(data=data, index=['All', 'Greater_Than_Average', 'Less_Than_Average'],
                      columns=['Max_Title', 'Avg_Title', 'Max_Word_Count', 'Avg_Word_Count',
		               'Noun_Phrases', 'Subjectivity', 'Polarity', 'Avg_Votes'])
    return df


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
                        args.start, args.end, args.verbose))

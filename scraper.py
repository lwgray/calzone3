#! /usr/bin/env python3

from functools import wraps

import os
import praw
import sqlite3
import time

TIMESTAMP_A = 1504657288
TIMESTAMP_B = 1507249288

# DEBUG
def timing(method):
    @wraps(method)
    def timed(*args, **kwargs):
            time_s = time.time()

            # TODO Write comment
            result = method(*args, **kwargs)

            time_e = time.time()

            print("Elapsed time: {0}".format(time_s - time_e))

            return result

    # TODO Write comment
    return timed

def format_data(submissions, subreddit = None):
	for data in submissions:
		yield data.id, subreddit, data.title, data.ups, data.url

try:
	from configparser import ConfigParser
except ImportError:
	from ConfigParser import ConfigParser # For Python versions prior to 3.0

config = ConfigParser()

# Ignore the possibility of this failing
config.read("config.ini")

reddit = praw.Reddit(
	# [client_data]
	client_id     = config["client_data"]["client_id"],
	client_secret = config["client_data"]["client_secret"],
	user_agent    = config["client_data"]["user_agent"],

	# [credentials]
	username = config["credentials"]["username"],
	password = config["credentials"]["password"]
)

if __name__ == "__main__":
	is_present = os.path.exists(config["DEFAULT"]["file"])
	subreddits = config["input"]["subreddits"].split('\n')
	
	with sqlite3.connect(config["DEFAULT"]["file"]) as connect:
		cursor = connect.cursor()
		
		if is_present != True:
			cursor.execute('''
				CREATE TABLE `submissions` (
					`id` PRIMARY KEY,
					`subreddit`,
					`title`,
					`ups`,
					`url`
				)
			''')
		
		# TODO Write comment
		for subreddit in [reddit.subreddit(name) for name in subreddits if name]:
			submissions = subreddit.submissions(TIMESTAMP_A, TIMESTAMP_B)
			
			# Prepare the collected data and submit it
			cursor.executemany('''
				INSERT OR IGNORE INTO `submissions`
				VALUES (?, ?, ?, ?, ?)
			''', format_data(submissions, subreddit.display_name))

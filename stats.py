#! /usr/bin/env python3

from urllib.request import urlopen

import sys

# subreddit

# /hot/
# /top/

if __name__ == "__main__":
	if len(sys.argv) != 3:
		quit()
	
	# Set the URL to the appropriate endpoint
	url = "https://www.reddit.com/r/{0}/{1}/.json".format(
		sys.argv[1], sys.argv[2]
	)
	
	# response = urlopen(url)
	# data = response.read()
	
	# print(data)
	# print(type(data))

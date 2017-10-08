#! /usr/bin/env python3

import urllib.request

# subreddit

# /hot/
# /top/

if __name__ == "__main__":
	if len(sys.argv) != 3:
		return
	
	# Set the URL to the appropriate endpoint
	url = "https://www.reddit.com/r/{0}/{1}/.json".format(
		sys.argv[1], sys.argv[2]
	)
	
	# urllib.request.urlopen(...)

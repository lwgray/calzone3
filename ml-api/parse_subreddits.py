# coding: utf-8
import csv
import pandas as pd
with open('subreddits.txt', 'r') as rd:
    reader = csv.reader(rd, delimiter='\n')
    answer =  [ line[0].split('/')[2] for line in reader]
    df = pd.DataFrame({'subreddit':answer})
    df.to_csv('subreddit.csv')
    

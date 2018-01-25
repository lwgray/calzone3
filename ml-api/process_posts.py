
# coding: utf-8

# In[89]:


import pandas as pd

def process(f_input, f_output):
    """Perform preprocessing on data.
       1. Add headers
       2. Remove Duplicate titles
       3. Remove subreddits without readable titles
       4. Remove subreddit specific words from titles 
    
    f_input csv: contains data downloaded from reddit
    f_output csv: file name to write processed data to
    
    """
    pd.set_option('display.float_format', lambda x: '%.1f' % x)
    try:
        data = pd.read_csv(f_input,
                           names=['id', 'subreddit', 'title', 'ups', 'url', 'created_utc'],
                           encoding = "ISO-8859-1")
    except:
        print('caught in reading')
    # Remove Duplicate Titles
    data.drop_duplicates('title', inplace=True)

    # Remove unwanted subreddit
    data = data[data['subreddit'] != 'r/me_irl']

    # Remove repetitive words from subreddit titles
    # for instance 'TIL' from r/todayilearned subreddit

    data.loc[data.subreddit=='r/todayilearned', 
             'title'] = data.loc[data['subreddit'] == 'r/todayilearned',
                                 'title'].str.replace('TIL', '')

    data.loc[data.subreddit=='r/photoshopbattles', 
             'title'] = data.loc[data['subreddit'] == 'r/photoshopbattles',
                                 'title'].str.replace('PsBattle:', '')
    try:
        data.to_csv('{0}.bz2'.format(f_output), index=False, compression='bz2', encoding='ISO-8859-1')
    except:
        print('caught in writing')
    return


# In[80]:


#for x in data.subreddit.unique():
#    print(data[data['subreddit'] == x][['subreddit', 'title']].head(1))


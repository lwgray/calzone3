
# coding: utf-8

# ### This Notebook is for feature analysis and addresses the following
# 1. Broad overview of the data we are working with
# 2. Evaluation of importance of each feature
# 
# #### In regards to feature analysis:
# We needed a way to determine which features to include in our analsys.
# Below you will find 3 graphs depicting the same information in different ways
# What we concluded from this analysis was that some features are highly correlated thus provide no additional information.
# Because of this, we have chosen to use only the features: wordcount, polarity, subjectivity, and noun-phrases

# In[1]:


"""Notebook showing Correlation heatmap for selected features"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
# get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
import seaborn as sns
from matplotlib import cm as cm
from textblob import TextBlob
from yellowbrick.features.rankd import Rank2D
from yellowbrick.text import FreqDistVisualizer
from feature_extraction import LemmaTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.simplefilter(action = "ignore", category = FutureWarning)


# In[2]:


# Read data
data = pd.read_csv('processed_datascience.csv.bz2')


# ### Exploratory Stats for Upvotes

# In[3]:


# Stats for Upvotes
print('Exploratory Stats for Upvotes')
print(data.ups.describe())

## Optional: Throw out outliers by including rows with Z-Scores less than 2.5 and greater than -2.5
data['z_scores'] = np.abs((data.ups-data.ups.mean())/data.ups.std())
data = data[data['z_scores']<= 2.5]

## Optional: Log transformation of up-votes
data['log_ups'] = np.log1p(data['ups'])


# Distribution of Upvotes
plt.figure(figsize=(12,8))
plt.subplot(2,2,1)
plt.title('Distribution of Upvotes')
plt.hist(data['ups'])
plt.xlabel('Upvotes per Post')

plt.subplot(2,2,2)
plt.title('Log Transformed Distribution of Upvotes')
plt.hist(data['log_ups'])
plt.xlabel('Upvotes per Post(log)')
plt.show()
plt.close()

# ### Create Features
# 1. WordCount - The number of words in the title
# 2. CharCount - the number of characters in the title
# 3. Vowels - The number of vowels in the title
# 4. Consonants - The number of consonants in the title
# 5. gtavg - The number of up-votes greater than the average number of up-votes per post
# 6. polarity - The positive or negative sentiment of the title
# 7. subjectivity - Measure of objectivity and subjectivity of each title
# 8. Noun Phrases - The number of nouns in each title

# In[4]:


# Generate and package data into dataframe
blobs = [TextBlob(sentence) for sentence in data.title]
data['polarity'] = [blob.sentiment.polarity for blob in blobs]
data['subjectivity'] = [blob.sentiment.subjectivity for blob in blobs]
data['noun_phrases'] = [len(blob.noun_phrases) for blob in blobs]

data['gtavg'] = data['ups'] > data.ups.mean()
data['wordcount'] = data['title'].str.split().apply(len)
data['charcount'] = data.title.str.len()
data['vowels'] = data.title.str.findall(r'[aeiou]').apply(len)
data['consonants'] = data.title.str.findall(r'[^aeiou]').apply(len)

df = data[['gtavg','wordcount','charcount','vowels','consonants', 'polarity', 'subjectivity', 'noun_phrases']]


# ### Plot Correlation heatmap - using Seaborn

# In[5]:


# plot corellation heatmap
corr = df.corr()
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns,cmap='jet')
plt.show()
plt.close()

# ### Show numerical correlation values

# In[6]:


# Show numerical values for correlation
cmap = cmap=sns.diverging_palette(5, 250, as_cmap=True)

def magnify():
    return [dict(selector="th",
                 props=[("font-size", "7pt")]),
            dict(selector="td",
                 props=[('padding', "0em 0em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                         ('font-size', '12pt')])
]

corr.style.background_gradient(cmap, axis=1)    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})    .set_caption("Hover to magify")    .set_precision(2)    .set_table_styles(magnify())


# ### Examine Pearson Correlation with Yellowbrick

# In[7]:


features = ['wordcount','charcount','vowels','consonants', 'polarity', 'subjectivity', 'noun_phrases']
X = data[features].as_matrix()
y = data['gtavg'].as_matrix()


# In[8]:


visualizer = Rank2D(features=features, algorithm='pearson', colormap='jet')
visualizer.fit(X,y)
visualizer.transform(X)
#visualizer.poof()
visualizer.poof()
plt.close()

# ### Frequency Distribution of unigram/bigrams in Corpus(post titles)

# In[13]:


vectorizer = TfidfVectorizer(ngram_range=(1,4),
                             sublinear_tf=True, stop_words='english',
                             max_df=0.5, min_df=10, strip_accents='unicode'
                            )

docs = vectorizer.fit_transform(data.title)
features = vectorizer.get_feature_names()


visualizer = FreqDistVisualizer(features=features, orient='v', n=50)
visualizer.fit(docs)
visualizer.poof()
plt.close()

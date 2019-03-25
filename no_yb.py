import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
from IPython.display import display, HTML

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline, FeatureUnion
from feature_extraction import Blob, Words, Exclude, WordCount, POS, Readable
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectPercentile, f_classif, SelectFromModel
from sklearn.preprocessing import MinMaxScaler, Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from calzone_keras import describe, lemmatize

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.optimizers import SGD
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
import numpy
import pandas
from sklearn.base import BaseEstimator, ClassifierMixin
import tensorflow as tf

#Read in posts

data = pd.read_csv('processed_datascience.csv.bz2')
data['title'] = lemmatize(data)


## Optional: Throw out outliers by including rows with Z-Scores less than 2.5 and greater than -2.5
data['z_scores'] = np.abs((data.ups-data.ups.mean())/data.ups.std())
data = data[data['z_scores']<= 2.5]

## Optional: Log transformation of up-votes
data['log_ups'] = np.log1p(data['ups'])

# Create Label column defining whether or not the article's votes exceed the average vote for the subreddit
data['gtavg'] = data.log_ups > data.log_ups.mean()
data['target'] = LabelEncoder().fit_transform(data.gtavg.values.ravel())

train_X, test_X, train_y, test_y = train_test_split(data.title, 
                                                    data.target, 
                                                    test_size=0.20,
                                                    random_state=25)
def keras_model():
    #optimizer = tf.train.RMSPropOptimizer(0.001)
    model = Sequential()
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop',
                  metrics=['accuracy'])
    #model.compile(loss='mean_squared_error', optimizer='sgd')

    return model

pipeline = Pipeline([
    ('union', FeatureUnion(
        transformer_list=[
                      
            ('pipe', Pipeline([
                ('inner', FeatureUnion(
                    transformer_list=[
                        ('pos', POS()),

                        ('read', Readable()),

                        ('words', Words()),

                        ('blob', Pipeline([
                            ('all', Blob()),
                            ('minmax', MinMaxScaler()),
                        ])),
                ])),
                ('select', SelectFromModel(ExtraTreesClassifier()))
   
            ])),
                      
            ('title', Pipeline([
                ('tfidf', TfidfVectorizer(token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', ngram_range=(1,3), sublinear_tf=True,
                                          strip_accents='unicode', stop_words='english')),
                ('svd', TruncatedSVD(n_components=120)),
                ('normalize', MinMaxScaler(copy=False)),
                ('selector', SelectPercentile(f_classif, percentile=10))
            ])),

            
            ])),
    ('clf', KerasClassifier(build_fn=keras_model, epochs=10)),
        ])
        
# Train model
pipeline.fit(train_X, train_y)

# Predict Test Set
y_pred = pipeline.predict(test_X)

# Test it out
print(pipeline.predict(
    pd.Series(['Data Lakes and Pipelines','hackhub','Looking for MOOCs with actual projects to add to Github/Resume','A tutorial on my machine-learning workflow for predicting whether or not this post will be popular']
    )))
    
# Save our model
joblib.dump(pipeline, 'datascience_keras_noYB.xz', compress=('xz', 9))
    
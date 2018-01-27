import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.pipeline import Pipeline, FeatureUnion
from feature_extraction import Blob, Words
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.preprocessing import MinMaxScaler, Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from time import time
from pprint import pprint
from sklearn.ensemble import RandomForestClassifier


grid = False 
data = pd.read_csv('processed_posts.csv.bz2')
#data = pd.read_csv('processed_datascience.csv.bz2', encoding='ISO-8859-1', compression='bz2')
data.drop_duplicates('title', inplace=True)

data['gt5'] = data['ups'] > 5
data['gt20'] = data['ups'] > 20
data['gt10'] = data['ups'] > 10
data['gt50'] = data['ups'] > 50
data['gt100'] = data['ups'] > 100

data = data[data['subreddit'] == 'r/funny']
train_X, test_X, train_y, test_y = train_test_split(data.title,
                                                    data.gt10,
                                                    test_size=0.20,
                                                    random_state=42)


print(data[data['gt10'] == False].shape)
print(data[data['gt10'] == True].shape)

pipeline = Pipeline([
    ('union', FeatureUnion(
        transformer_list=[

            ('words', Words()),

            ('title', Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1, 3),
                                          sublinear_tf=True,
                                          stop_words='english')),
                ('svd', TruncatedSVD(n_components=120)),
                ('normalize', MinMaxScaler(copy=False)),
                ('selector', SelectPercentile(f_classif, percentile=10))
            ])),

            ('blob', Pipeline([
                ('all', Blob()),
                ('minmax', MinMaxScaler()),
            ])),

            ])),
    ('clf', RandomForestClassifier(n_estimators=1200, max_depth=30, min_samples_split=5,
                                   min_samples_leaf=5, max_features='sqrt')),
        ])


parameters = {
    'clf__n_estimators': (120, 300, 500, 800, 1200),
    'clf__max_depth': (5, 8, 15, 25, 30, None),
    'clf__min_samples_split': (2, 5, 10, 15, 100),
    'clf__min_samples_leaf': (1, 2, 5, 10),
    'clf__max_features': ('log2', 'sqrt', None),
}

if grid is True:
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(train_X, train_y)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))


    y = grid_search.predict(test_X)
    accuracy_score(y_pred=y, y_true=test_y)

if grid is False:
    print('Fitting Classifier')
    pipeline.fit(train_X, train_y)
    y = pipeline.predict(test_X)
    print(accuracy_score(y_pred=y, y_true=test_y))
    # cross_val_score(pipeline, train_X, train_y, cv=5)

    index = 2
    print (test_X.iloc[index])
    print (test_y.iloc[index])
    print (y[index])
    pipeline.predict(pd.Series(['My Job Search as a PhD Student']))[0]

'''
data.to_csv('gt_politics.csv', index=False)


pipeline = Pipeline([
    ('union', FeatureUnion(
        transformer_list=[

            ('wordcount', WordCount()),

            ('charcount', CharCount()),

            ('title', TfidfVectorizer(ngram_range=(1,4))),

            ('vowel', Vowels()),

            ('consonants', Consonants()),

            ('polarity', Polarity()),

            ('subjectivity', Subjectivity()),

            ('noun_phrases', Nouns()),

            ])),
    ('clf', ExtraTreesClassifier()),
        ])
'''

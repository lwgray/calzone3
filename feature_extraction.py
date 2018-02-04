''' Extractors for Reddit Titles '''
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from textblob import TextBlob


class DataExtractor(BaseEstimator, TransformerMixin):
    """ Select Title """
    def fit(self, x, y=None):
        return self

    def transform(self, df):
        return df[['title']]


class ItemSelector(BaseEstimator, TransformerMixin):
    """ Select Feature """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


class WordCount(BaseEstimator, TransformerMixin):
    """ Extract number of words in title"""

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        df = pd.DataFrame({'wordcount': titles.str.split().apply(len)})
        return df['wordcount'].values.reshape(-1, 1)


class CharCount(BaseEstimator, TransformerMixin):
    """ Extract number of words in title"""

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        df = pd.DataFrame({'charcount': titles.str.len()})
        return df['charcount'].values.reshape(-1, 1)


class Vowels(BaseEstimator, TransformerMixin):
    """ Extract number of words in title"""

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        df = pd.DataFrame({'vowels': titles.str.findall(r'[aeiou]').apply(len)})
        return df['vowels'].values.reshape(-1, 1)


class Consonants(BaseEstimator, TransformerMixin):
    """ Extract number of words in title"""

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        df = pd.DataFrame({'consonants': titles.str.findall('r[^aeiou]').apply(len)})
        return df['consonants'].values.reshape(-1, 1)


class Polarity(BaseEstimator, TransformerMixin):
    """ Determine sentiment polarity """

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        blobs = [TextBlob(sentence) for sentence in titles]
        polarity = [blob.sentiment.polarity for blob in blobs]
        df = pd.DataFrame({'polarity': polarity})
        return df.polarity.values.reshape(-1, 1)


class Subjectivity(BaseEstimator, TransformerMixin):
    """ Determine sentiment polarity """

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        blobs = [TextBlob(sentence) for sentence in titles]
        subjectivity = [blob.sentiment.subjectivity for blob in blobs]
        df = pd.DataFrame({'subjectivity': subjectivity})
        return df.subjectivity.values.reshape(-1, 1)


class Nouns(BaseEstimator, TransformerMixin):
    """ Extract number of nouns in title """

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        blobs = [TextBlob(sentence) for sentence in titles]
        noun_phrases = [len(blob.noun_phrases) for blob in blobs]
        df = pd.DataFrame({'noun_phrases': noun_phrases})
        return df.noun_phrases.values.reshape(-1, 1)


class Blob(BaseEstimator, TransformerMixin):
    """ Combine noun, subject, polar extractors """

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        blobs = [(len(x.noun_phrases), x.sentiment.subjectivity, x.sentiment.polarity) for x in [TextBlob(sentence) for sentence in titles]]
        return blobs


class Words(BaseEstimator, TransformerMixin):
    """ Combine Vowels,Consonants, CharCount, and WordCount extractors """

    def fit(self, x, y=None):
        return self

    def transform(self, titles):
        words = list(zip(titles.str.findall('r[aeiou]').apply(len),
                         titles.str.findall('r[^aeiou]').apply(len),
                         titles.str.len(),
                         titles.str.split().apply(len)))
        return words

# coding: utf-8
import pickle
from nltk.corpus import stopwords

docs = pickle.load(open('training_data.p', 'rb'))
data = [value['resolved_title'] for info in docs for key, value in info.iteritems()]
texts = [[word for word in datum.lower().split() if word not in stopwords.words('english')] for datum in data]

print data[0]
print texts[0]

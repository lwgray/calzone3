#! /usr/bin/env python

from flask import Flask
from flask_cors import CORS
import urllib2
import pickle
import scipy
import numpy
app = Flask(__name__)
CORS(app)
def apply(input):
    path1 = "bow_transformer_v1.pkl"
    path2 = "tfidf_transformer_v1.pkl"
    path3 = "lsa_v1.pkl"
    path4 = "prediction_model_v1.pkl"
    bow = pickle.load(open(path1, 'rb'))
    bow_tf = bow.transform([input])
    tfidf = pickle.load(open(path2,'rb'))
    tfidf_tf = tfidf.transform(bow_tf)
    lsa = pickle.load(open(path3,'rb'))
    lsa_tf = lsa.transform(tfidf_tf)
    model4 = pickle.load(open(path4,'rb'))
    prediction = model4.predict(lsa_tf).tolist()
    return str(prediction[0])

@app.route("/rating/<query>")
def bar(query):
        return str(apply(query))


def go_to(page, subreddit):
	url = "https://www.reddit.com/r/{0}/{1}/.json".format(
		subreddit, page
	)
	
	response = urllib2.urlopen(url)
	returnMe = response.read()
	
	return returnMe

@app.route("/hot/<subreddit>")
def foo(subreddit):
	content = go_to("hot", subreddit)
	
	# TODO Do something with the content
	
	# DEBUG
	return "/top/" + str(subreddit) + '\n'

@app.route("/top/<subreddit>")
def goo(subreddit):
	content = go_to("top", subreddit)
	
	# TODO Do something with the content
	
	# DEBUG
	return "/top/" + str(subreddit) + '\n'

if __name__ == "__main__":
	app.run("0.0.0.0")


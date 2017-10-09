from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import urllib2
import json
import praw
import pickle
import sklearn
#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

reddit = praw.Reddit(client_id='kZLtaDQZnQAcrw',
                    client_secret='cJhtGj9LEdBj5PK6AnMRQLgb7xQ',
                    password='vasanth9876',
                    user_agent='RedditApiClient/0.1 by Vasanth',
                    username='vk432')
subreddit='all'

e = create_engine('sqlite:///redditposts.db')

app = Flask(__name__)
api = Api(app)
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

@app.route('/articles/<articleid>')
def api_article(articleid):
    return  apply(articleid)

class Run_Calc(Resource):
    def get(self):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select distinct title from posts")
        return {'posts': [i[0] for i in query.cursor.fetchall()]}

api.add_resource(Run_Calc, '/machine_learn')

if __name__ == '__main__':
     app.run(host='0.0.0.0')

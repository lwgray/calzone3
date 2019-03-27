#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request
from sklearn.externals import joblib
import pandas as pd

#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/getdelay',methods=['POST','GET'])
def get_delay():
    if request.method == 'POST':
        result = request.form
        # logmodel = joblib.load('datascience_keras_noYB.xz')
        logmodel = joblib.load('ds.xz')
        prediction = logmodel.predict(pd.Series([result['query']]))
        return render_template('result.html', prediction=prediction, query=result['query'])

if __name__ == '__main__':
    app.run(debug=True)

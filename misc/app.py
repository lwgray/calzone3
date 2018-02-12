from flask import Flask, render_template, request
from sklearn.externals import joblib
from flask_restful import Resource, Api, reqparse
import pandas as pd
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm


app = Flask(__name__)
api = Api(app)
Bootstrap(app)

'''
class MyForm(FlaskForm):
    title_line = StringField('Title', validators=[DataRequired()])
    submit = SubmitField("Send")


@app.route('/index', methods=['POST'])
@app.route('/', methods=['POST'])
def index():
    form = MyForm()
    if request.method == "POST":
        title = pd.Series([form.title.data])
        answer = clf.predict(title[0])
        # return render_template('index.html', form=form, prediction=answer)
        return 'hello world'
    else:
        # return render_template('index.html')
        return 'hello else'
@app.route('/dog', methods=['POST'])
def dog():
    if request.method == "POST":
        return 'hello dog'


'''
class Prediction(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Title of post')
        args = parser.parse_args()

        print(args['title'])
        prediction = str(pipeline.predict(pd.Series(args['title']))[0])

        print("The Prediction is {0}".format(prediction))

        return {
                'prediction': prediction
               }


api.add_resource(Prediction, '/prediction')

if __name__ == '__main__':
    pipeline = joblib.load('datascience.pkl')
    app.run(debug=True, host='0.0.0.0')

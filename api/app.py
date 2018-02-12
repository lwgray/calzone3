from chalice import Chalice
import pandas as pd
import hashlib
from sklearn.externals import joblib


app = Chalice(app_name='test1')


@app.route('/')
def index():
    return {'response': 'OK'}

"""
@ap p.route('/predict/{title}')
def predict_it(title):
    pipeline = joblib.load('../datascience.pkl')
    prediction = pipeline.predict(pd.Series([title]))
    return {'response': prediction}
"""

@app.route('/md5/{string_to_hash}')
def hash_it(string_to_hash):
    m = hashlib.md5()
    m.update(string_to_hash.encode("UTF-8"))
    return {'response': str(m.hexdigest())}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

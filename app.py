from flask import Flask, request, url_for, render_template, jsonify, redirect
from requests import Response

import settings
from garmin_api.core import GarminApi

app = Flask(__name__)
app.secret_key = 'AHUIHSUHASU151465IYASBI'  # 隨便打
app.config['SESSION_TYPE'] = 'filesystem'

garmin_api = GarminApi(app)

#
# ---
#

@app.route('/')
def hello_world():
    return \
        '<a href="/login">Login</a> <br>' + \
        '<a href="daily_summaries">Get daily_summaries</a>'

#
# oauth
#

@app.route('/login')
def login():
    return garmin_api.route_login()

@app.route('/authorize')
def authorize():
    return garmin_api.route_authorize()


#
# callback
#

# @app.post('/callback')
# def callback():
#     # TODO...
#     print(len(request.values))
#     return 'ok'

#
# API
#
@app.get('/daily_summaries')
def test1():
    return garmin_api.get_daily_summaries()


if __name__ == '__main__':
    app.run()

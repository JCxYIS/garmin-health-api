import logging

from flask import Flask, request, url_for, render_template, jsonify, redirect, abort
from requests import Response

import settings
import garmin_api.const as const
from garmin_api.core import GarminApi

app = Flask(__name__)
app.secret_key = settings.FLASK_SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

logging.basicConfig(format='%(asctime)s | %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.DEBUG)
garmin_api = GarminApi(app)



#
# ---
#

@app.route('/')
def hello_world():
    return render_template('index.html')


#
# oauth
#

@app.route('/login')
def login():
    return garmin_api.route_login()


@app.route('/authorize')
def authorize():
    return garmin_api.route_authorize()


@app.route('/logout')
def logout():
    return garmin_api.route_logout()


#
# callback
#

@app.post('/callback/<callback_name>')
def callback(callback_name: str):
    try:
        print('callback at endpoint=', callback_name)
        print(request.data, flush=True)
        print(request.json, flush=True)
    except Exception as e:
        print('callback error!', e)
    return 'ok'


#
# API
#


@app.get('/api/health/<data_name>')
def get_health_api(data_name: str):
    try:
        return garmin_api.get_data(data_name,
                                   request.args.get('start', type=int),
                                   request.args.get('end', type=int))
    except ModuleNotFoundError:
        return abort(404, f"Data name \"{data_name}\" is invalid.")
    # return data_name


if __name__ == '__main__':
    app.run()

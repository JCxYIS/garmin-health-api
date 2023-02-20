import datetime
import json
import logging

from flask import Flask, request, url_for, render_template, jsonify, redirect, abort
from requests import Response

import settings
import garmin_api.const as const
from garmin_api.core import GarminApi
from db.mongo_db_service import MongoDbService

app = Flask(__name__)
app.secret_key = settings.FLASK_SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

logging.basicConfig(format='%(asctime)s | %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.DEBUG)
garmin_api = GarminApi(app)
mongodb = MongoDbService(settings.MONGO_CONNECTION_STRING)


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

callback_history = []

@app.post('/callback/<callback_name>')
def callback(callback_name: str):
    """
    Garmin API callback

    :param callback_name:
    :return:
    """
    try:
        print('callback at endpoint=', callback_name)

        callback_history.append({
            "callback_name": callback_name,
            "callback_time": int(datetime.datetime.timestamp(datetime.datetime.now())),
            "data": request.data.decode("utf-8") if request.data is not None else '',
        })

        json_data = request.json
        for data_name in json_data:  # should only run once (loop 0 time)
            print(f'--data_name={data_name} | data_count={len(json_data[data_name])}')
            for data in json_data[data_name]:  # 1 or more
                # print()
                mongodb.add_data(data_name, data)
        # print(request.json, flush=True)
        print(flush=True)
    except Exception as e:
        print('catch callback error!', e)
    return 'ok'

# @app.get('/cbhistory/ciph')
# def cbhistory_ciph():
#     return jsonify(callback_history)

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

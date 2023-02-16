from flask import Flask, request, url_for, render_template, jsonify, redirect
from requests import Response

import settings
from garmin_api.core import GarminApi

app = Flask(__name__)
app.secret_key = settings.FLASK_SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

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
@app.get('/daily_summaries')
def test1():
    return garmin_api.get_daily_summaries()

@app.get('/third_party_daily_summaries')
def test2():
    return garmin_api.get_third_party_daily_summaries()

@app.get('/epoch_summaries')
def test3():
    return garmin_api.get_epoch_summaries()

@app.get('/sleep_summaries')
def test4():
    return garmin_api.get_sleep_summaries()

@app.get('/composition_summaries')
def test5():
    return garmin_api.get_composition_summaries()

@app.get('/stress_details_summaries')
def test6():
    return garmin_api.get_stress_details_summaries()

@app.get('/user_metrics_summaries')
def test7():
    return garmin_api.get_user_metrics_summaries()

@app.get('/pulse_ox_summaries')
def test8():
    return garmin_api.get_pulse_ox_summaries()

@app.get('/respiration_summaries')
def test9():
    return garmin_api.get_respiration_summaries()

@app.get('/health_snapshot_summaries')
def test10():
    return garmin_api.get_health_snapshot_summaries()

@app.get('/heart_rate_variability_summaries')
def test11():
    return garmin_api.get_heart_rate_variability_summaries()

@app.get('/blood_pressure_summaries')
def test12():
    return garmin_api.get_blood_pressure_summaries()


if __name__ == '__main__':
    app.run()

import logging
from datetime import datetime, timedelta, tzinfo
from zoneinfo import ZoneInfo

from authlib.integrations.flask_client import OAuth, FlaskOAuth1App
from flask import url_for, request, make_response, redirect, Flask
from requests import Response

import settings
from garmin_api.const import *

_logger = logging.getLogger(__name__)

class GarminApi:
    oauth: OAuth
    oauth_client = None
    garmin: FlaskOAuth1App

    token_secret_dict = {}  # [{oauth_token: oauth_token_secret, ...]

    def __init__(self, app: Flask):
        # setup oauth
        self.oauth = OAuth(app)
        self.oauth_client = self.oauth.register(
            name='garmin',
            client_id=settings.CONSUMER_KEY,
            client_secret=settings.CONSUMER_SECRET,
            request_token_url='https://connectapi.garmin.com/oauth-service/oauth/request_token',
            authorize_url='https://connect.garmin.com/oauthConfirm',
            access_token_url='https://connectapi.garmin.com/oauth-service/oauth/access_token',
        )
        self.garmin = self.oauth.create_client('garmin')

        # pre-fill oauth dict for test (=> no need to login every time)
        self.token_secret_dict = settings.TOKEN_SECRET_DICT

    """
    Routes
    """

    def route_login(self):
        redirect_uri = url_for('authorize', _external=True)
        return self.garmin.authorize_redirect(redirect_uri)

    def route_authorize(self):
        token = self.oauth_client.authorize_access_token()  # {'oauth_token': 'xxx', 'oauth_token_secret': 'xxx'}
        # you can save the token into database
        resp = make_response(redirect('/'))
        resp.set_cookie('oauth_token', token['oauth_token'])
        self.token_secret_dict[token['oauth_token']] = token['oauth_token_secret']
        _logger.debug(self.token_secret_dict)
        return resp

    def route_logout(self):
        token_token = request.cookies.get('oauth_token')
        resp = make_response(redirect('/'))
        if token_token is not None:
            self.token_secret_dict[token_token] = None
        resp.delete_cookie('oauth_token')
        return resp

    """
    func
    """

    def get_token(self):
        """
        Get token & secret from local source, if not found, return None.

        :return: {'oauth_token': token, 'oauth_token_secret': token_secret }
        """
        token_token = request.cookies.get('oauth_token')
        token_secret = self.token_secret_dict.get(token_token)
        if token_token is None or token_secret is None:
            return None
        return {'oauth_token': token_token, 'oauth_token_secret': token_secret}

    """
    api
    """

    def call_api(self, endpoint: str, start_time=None, end_time=None):
        """
        Call garmin api.

        :param endpoint: api endpoint (e.g. activities)
        :param start_time: start timestamp. Default to last 24hrs
        :param end_time: end time stamp. Default to now
        :return:
        """
        token = self.get_token()
        if token is None:
            return {'error': 'Not logged in.'}

        if start_time is None and end_time is None:
            now = datetime.utcnow() + timedelta(hours=8)  # TODO: this is only for Taiwan Timezone (UTC+8). You may want to change this
            start_time = int((now - timedelta(days=1)).timestamp())
            end_time = int(now.timestamp())

        url = f'{API_HOST}/{endpoint}?uploadStartTimeInSeconds={start_time}&uploadEndTimeInSeconds={end_time}'
        resp: Response = self.garmin.get(url, token=token)
        _logger.debug('request url:', url, 'response code:', resp.status_code)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            return {'error': 'Invalid login data. Please login again.'}
        elif resp.status_code == 400:
            _logger.warn(resp.content)
            return {'error': 'Bad Request: ' + resp.json()['errorMessage']}
        else:
            _logger.error(resp.content)
            return {'error': 'Unknown Error'}


    def get_daily_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_DAILY_SUMMARIES, start_time, end_time)

    def get_third_party_daily_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_THIRD_PARTY_DAILY_SUMMARIES, start_time, end_time)

    def get_epoch_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_EPOCH_SUMMARIES, start_time, end_time)

    def get_sleep_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_SLEEP_SUMMARIES, start_time, end_time)

    def get_composition_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_COMPOSITION_SUMMARIES, start_time, end_time)

    def get_stress_details_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_STRESS_DETAILS_SUMMARIES, start_time, end_time)

    def get_user_metrics_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_USER_METRICS_SUMMARIES, start_time, end_time)

    def get_pulse_ox_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_PULSE_OX_SUMMARIES, start_time, end_time)

    def get_respiration_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_RESPIRATION_SUMMARIES, start_time, end_time)

    def get_health_snapshot_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_HEALTH_SNAPSHOT_SUMMARIES, start_time, end_time)

    def get_heart_rate_variability_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_HEART_RATE_VARIABILITY_SUMMARIES, start_time, end_time)

    def get_blood_pressure_summaries(self, start_time=None, end_time=None):
        return self.call_api(API_BLOOD_PRESSURE_SUMMARIES, start_time, end_time)

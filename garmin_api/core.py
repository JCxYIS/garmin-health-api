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

    def call_api(self, endpoint: str, start_time: int = None, end_time: int = None):
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

        now = datetime.utcnow() + timedelta(hours=8)  # TODO: Taiwan Timezone (UTC+8). You may want to change this.
        if start_time is None:
            start_time = int((now - timedelta(days=1)).timestamp())
        if end_time is None:
            end_time = int(now.timestamp())

        url = f'{API_HOST}/{endpoint}?uploadStartTimeInSeconds={start_time}&uploadEndTimeInSeconds={end_time}'
        resp: Response = self.garmin.get(url, token=token)
        _logger.debug('Request url: %s | response code: %s | Timestamp: %s ~ %s',
                      url, resp.status_code, datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time))
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            return {'error': 'Invalid login data. Please login again.'}
        elif resp.status_code == 400:
            _logger.warning(resp.content)
            return {'error': 'Bad Request: ' + resp.json()['errorMessage']}
        else:
            _logger.error(resp.content)
            return {'error': 'Unknown Error'}

    def get_data(self, data_name: str, start_time=None, end_time=None):
        """
        call api by data_name

        :param data_name:
        :param start_time: start timestamp. Default to last 24hrs
        :param end_time: end time stamp. Default to now
        :return:
        """
        endpoint = API_HEALTH_ENDPOINTS.get(data_name)
        if endpoint is None:
            raise ModuleNotFoundError()
        return self.call_api(endpoint, start_time, end_time)

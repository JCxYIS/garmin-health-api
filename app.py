from flask import Flask, request, url_for, render_template, jsonify, redirect
from authlib.integrations.flask_client import OAuth

import settings

app = Flask(__name__)
app.secret_key = 'AHUIHSUHASU151465IYASBI'  # 隨便打
app.config['SESSION_TYPE'] = 'filesystem'
oauth = OAuth(app)
garmin_oauth = oauth.register(
    name='garmin',
    client_id=settings.CONSUMER_KEY,
    client_secret=settings.CONSUMER_SECRET,
    request_token_url='https://connectapi.garmin.com/oauth-service/oauth/request_token',
    authorize_url='https://connect.garmin.com/oauthConfirm',
    access_token_url='https://connectapi.garmin.com/oauth-service/oauth/access_token',
)
garmin = oauth.create_client('garmin')

@app.route('/')
def hello_world():
    return '<a href="/login">login</b>'

#
# oauth
#

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return garmin.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = garmin_oauth.authorize_access_token()
    # you can save the token into database
    print(token)
    return redirect('/')
    # profile = garmin('/user', token=token)
    # return jsonify(profile)


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
@app.get('/test1')
def test1():
    # TODO...
    pass


if __name__ == '__main__':
    app.run()

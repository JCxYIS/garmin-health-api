import os
from dotenv import load_dotenv

load_dotenv()

# Garmin API Keys
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

# Flask Secret key
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

#
MONGO_CONNECTION_STRING = os.environ['MONGO_CONNECTION_STRING']

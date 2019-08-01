import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY') or 'YOUR TWITTER DEVELOPER CONSUMER KEY'
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') or 'TOUR TWITTER DEVELOPER CONSUMER SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

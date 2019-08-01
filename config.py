import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY') or 'kd8Mq1XlxRnjMH4xdWxReBXKm'
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') or 'oBmGcMYkkYC4Cs45Bam3Uf0qTSaBi7KnC7DPAKKDIJMP6VgOVi'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

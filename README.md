# twygator
Twygator aggregates 5 most recent statuses from each of your friends and present it to you so that you can keep yourself up-to-date with your friends' timelines in a few glances!

To use twygator locally:

1. Download all files however you want into your computer.
2. In the outmost level, same as README.md, create a "config.py" file, and Copy the following:
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY') or 'YOUR TWITTER API CONSUMER KEY'
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') or 'YOUR TWITTER API CONSUMER SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
3. Open Command Prompt and navigate to the location of the folder.
4. enter "flask run".
5. Open your browser and enter the local url assigned.

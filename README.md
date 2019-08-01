# Twygator
Twygator aggregates 5 most recent statuses from each of your friends and present it to you so that you can keep yourself up-to-date with your friends' timelines in a few glances!

## Getting Started

Twygator is not deployed yet, so you have to run it locally on your computer with the following instruction.

### Prerequisites
Since I stored my Twitter API key in my config.py file, you need to create yours to make twygator work. More on this later in the detailed instruction.
```
create a config.py the same level as README.md
```

### Use Twygator Locally:

1. Download all files however you want into your computer.
2. In the outmost level, same as README.md, create a "config.py" file, and Copy the following:
```
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY') or 'YOUR TWITTER API CONSUMER KEY'
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') or 'YOUR TWITTER API CONSUMER SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
3. In config.py, replace YOUR TWITTER API COMSUMER KEY and YOUR TWITTER API CONSUMER SECRET with your consumer key and secret.
4. Open Command Prompt and navigate to the location of the folder.
5. enter "flask run".
6. Open your browser and enter the local url assigned.

## Running the tests

To be added...

## Built With

* [Flask](https://palletsprojects.com/p/flask/) - the python web framework used
* [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Database used
* [flask-paginate](https://pythonhosted.org/Flask-paginate/) - Pagination extension on flask
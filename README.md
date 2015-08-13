# Knowledge Store Authentication Workaround app

A Flask app that proxies sparql requests to the Knowledge Store.

The Flask app requires Python 2.7 and pip.

The app runs on [https://shrouded-gorge-9256.herokuapp.com/](https://shrouded-gorge-9256.herokuapp.com/)

## Local Installation

    git clone git@github.com:jvdzwaan/visun-flask.git
    cd visun-flask
    pip install -r requirements.txt

## Run

In de `visun-flask` directory run:

    python server.py

Don't forget to change the url to the Knowledge Store to `http://0.0.0.0:5000/`

## Deploy on heroku

[https://devcenter.heroku.com/articles/getting-started-with-python-o#deploy-your-application-to-heroku](https://devcenter.heroku.com/articles/getting-started-with-python-o#deploy-your-application-to-heroku)

from flask import Flask
import psycopg2
from os import path


def create_app():
    # configure app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'TrackC String'


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Transaction
    
    return app


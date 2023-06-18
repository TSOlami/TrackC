from flask import Flask
import psycopg2
from os import path
from flask_login import LoginManager

def create_app():
    # configure app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'TrackC String'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Transaction

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader 
    def load_user(id):
        return User.query.get(int(id))   
    
    return app


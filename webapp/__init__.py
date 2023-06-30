from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import ApplicationConfig
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    # configure app
    app = Flask(__name__)

    app.config.from_object(ApplicationConfig)
    
    # Initialize the SQLAlchemy extension
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Transaction
    
    
    # Create the database tables
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == 'None':
            # handle the case where user_id is None
            # This means the user is a guest
            return None
        user = User.query.get(user_id)
        return user  

    return app

def create_database(app):
    """Create database tables if they don't exist"""
    with app.app_context():
        if not db.engine.dialect.has_table(db.engine, 'transactions') or not db.engine.dialect.has_table(db.engine, 'users'):
            db.create_all()
            print('Created Database!')
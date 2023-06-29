from flask import Flask
from flask_session import Session
from flask_cors import CORS
from .config import ApplicationConfig


def create_app():
    # configure app
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    app.config.from_object(ApplicationConfig)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import db
    
    # Initialize the SQLAlchemy extension
    db.init_app(app)
    server_session = Session(app)
    
    # Create the database tables
    with app.app_context():
        db.create_all()

    return app

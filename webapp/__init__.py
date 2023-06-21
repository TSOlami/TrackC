from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://juuthoos:GaAe2ZbZU77KorqGd7NgIJKfm5Ya9EpH@dumbo.db.elephantsql.com/juuthoos")
Session = sessionmaker(bind=engine)
session = Session()

def create_app():
    # configure app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'TrackC String'
    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://juuthoos:GaAe2ZbZU77KorqGd7NgIJKfm5Ya9EpH@dumbo.db.elephantsql.com/juuthoos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Base, User, Transaction

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader 
    def load_user(user_id):
        if user_id == 'None':
            # handle the case where user_id is None
            # This means the user is a guest
            return None
        user = session.query(User).get(user_id)
        return user  

    return app

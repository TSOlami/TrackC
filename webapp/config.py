from dotenv import load_dotenv
import os

load_dotenv()

class ApplicationConfig:
    
    SECRET_KEY = os.environ["SECRET_KEY"]
    
    # Configure the Flask app to use the PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://juuthoos:GaAe2ZbZU77KorqGd7NgIJKfm5Ya9EpH@dumbo.db.elephantsql.com/juuthoos'
    #SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


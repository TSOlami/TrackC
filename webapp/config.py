from dotenv import load_dotenv
import os

load_dotenv()


class ApplicationConfig:
    # secret key
    SECRET_KEY = os.environ["SECRET_KEY"]
    # password reset token expiration
    # Reset token expiration time in seconds
    RESET_TOKEN_EXPIRATION = os.environ["RESET_TOKEN_EXPIRATION"]
    # Gmail configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465  # TLS port
    MAIL_USE_TLS = False  # Enable TLS
    MAIL_USE_SSL = True  # Enable SSL
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    
    # Configure the Flask app to use the PostgreSQL database
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_ECHO = os.environ["SQLALCHEMY_ECHO"]
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]

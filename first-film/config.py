import os
import datetime


app_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG       = False
    TESTING     = False
    DEVELOPMENT = False

    FILMS_PER_PAGE = 24
    ENTRIES_PER_PAGE = 25

    SESSION_PROTECTION = 'basic' #'strong'
    SESSION_PERMANENT = True
    # REMEMBER_COOKIE_DURATION = datetime.timedelta(seconds=10)
    # PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=60*60)
    SESSION_REFRESH_EACH_REQUEST = True

    CREATE_DB = False


class ProductionConfig(Config):
    ENV          = 'production'
    CSRF_ENABLED = True
    SECRET_KEY   = os.environ.get('APP_SECRET_KEY')
    
    POSTGRES_IP       = os.environ.get('POSTGRES_IP')
    POSTGRES_DB       = os.environ.get('POSTGRES_DB')
    POSTGRES_USER     = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}/{POSTGRES_DB}'

    SQLALCHEMY_ECHO = False  
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV            = 'development'
    DEBUG          = True
    SECRET_KEY     = os.environ.get('APP_SECRET_KEY', '1234567890')
    DEVELOPMENT    = True
    CSRF_ENABLED   = True
    LOGIN_DISABLED = False
    
    POSTGRES_IP       = os.environ.get('POSTGRES_IP')
    POSTGRES_DB       = os.environ.get('POSTGRES_DB')
    POSTGRES_USER     = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

    # POSTGRES_IP = 'postgres'
    
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/firstFilm'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/first_film'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}/{POSTGRES_DB}'
    
    SQLALCHEMY_ECHO = False  
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir, 'app.db')
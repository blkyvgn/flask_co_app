from dotenv import dotenv_values
from kombu import Exchange, Queue
from flask_babel import lazy_gettext as _l

env = dotenv_values('.env')

class Config:
    TESTING = False

class DevelopmentConfig(Config):
    APP_NAME = env.get('APP_NAME', 'Flask App')
    DEBUG = env.get('DEBUG', False)
    SECRET_KEY = '*** change me please ***'
    COMPANY_ALIAS = 'grkr'

    SQLALCHEMY_DATABASE_URI = env.get('SQLITE_DATABASE_URI', 'sqlite:///./flask_co_db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGIN_MESSAGE = None

    # UPLOAD_FOLDER = 'app/storage/media' - set link from dir public to dir app/storage
    UPLOAD_FOLDER = 'media'
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    THUMBNAIL_WIDTH = 80
    MAX_CONTENT_LENGTH = 16 * 10000 * 10000

    IMAGE_WIDTH = {
        'THUMBNAIL': 60,
        'SHOWCASE': 220,
        'SLIDER': 500,
        'LOGO': 170,
    }

    DEFAULT_IMAGE = {
        'PLACEHOLDER': 'images/default/placeholder.png',
        'LOGO':        'images/default/logo.png',
        'ICON':        'images/default/icon.png',
        'USER':        'images/default/user.png',
    }

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    TRANSLATION_DIRECTORY = 'resources/translations'
    # BABEL_TRANSLATION_DIRECTORIES = '' Set in utility config
    ACCEPT_LANGUAGES = ['en', 'ru',]
    # available languages 
    LANGUAGES = { 
        'en': _l('English'),
        'ru': _l('Russian'),
    }

    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

    CACHE_TIMEOUT = {
        'YEAR':         60 * 60 * 24 * 364,
        'MONTH':        60 * 60 * 24 * 364,
        'DAY':          60 * 60 * 24 * 364,
        'FIVE_MINUTES': 60 * 60 * 5
    }

    PASSWD_LENGTH = {'MIN': 8, 'MAX': 16}

    USERNAME_LENGTH = {'MIN': 4, 'MAX': 24}
    COMMENT_TEXT_LENGTH = {'MIN': 12, 'MAX': 220}

    NUMBER_PER_PAGE = 15
    MAX_PER_PAGE = 15

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_USERNAME = ''# None
    MAIL_PASSWORD = ''# None
    MAIL_DEFAULT_SENDER = 'admin@mail.com'
    # MAIL_MAX_EMAILS = None
    # MAIL_SUPPRESS_SEND = True
    # MAIL_ASCII_ATTACHMENTS = False

    CELERY_BROKER_URL = 'redis://0.0.0.0:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://0.0.0.0:6379/0'
    result_backend = 'redis://0.0.0.0:6379/0'

    broker_transport = 'redis://0.0.0.0:6379/0'
    broker = 'redis://0.0.0.0:6379/0'
    result_backend = 'redis://0.0.0.0:6379/0'
    task_serializer = 'json'
    accept_content = ['json',]

    task_queues = (
        Queue('high', Exchange('high'), routing_key='high'), 
        Queue('normal', Exchange('normal'), routing_key='normal'), 
        Queue('low', Exchange('low'), routing_key='low'),
    ),
    task_default_queue = 'normal'
    task_default_exchange = 'normal'
    task_default_routing_key = 'normal'
    task_routes = {
        # -- HIGH PRIORITY QUEUE -- #
        # -- NORMAL PRIORITY QUEUE -- # 
        'app.tasks.mail.send_async_email': {'queue': 'normal'}
        # -- LOW PRIORITY QUEUE -- #
    }

    LOG_DIR = 'log'
    LOG_LEVELS = ['info', 'warning', 'error', 'critical']
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d'
    LOG_TYPE_INTERVAL = 'D'
    LOG_INTERVAL = 1
    LOG_BACKUP_COUNT = 0


class ProductionConfig(Config):
  pass

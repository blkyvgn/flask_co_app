from app.vendors.base.database import (
	AppModel,
	AppSession,
)
from app.vendors.helpers.config import cfg

# Auth
from flask_login import LoginManager
login_manager = LoginManager()

# Localization
from flask_babel import Babel
babel = Babel()

# Database
from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy(
	model_class=AppModel,
	session_options={'class_': AppSession}
)

from flask_migrate import Migrate
migrate = Migrate()

# Logger
import logging
logger = logging.getLogger()

# CSRF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

# Mail
from flask_mail import Mail
mail = Mail()

# Cache
from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

from flask_restful import Api
api = Api()

from flask_jwt_extended import JWTManager
jwt = JWTManager()

from flask_marshmallow import Marshmallow
marshmallow = Marshmallow()

from flask_socketio import SocketIO
socketio = SocketIO(async_mode='eventlet')


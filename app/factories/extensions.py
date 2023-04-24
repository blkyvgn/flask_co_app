from app.vendors.helpers import locale
from app.extensions import (
	login_manager, 
	babel,
	db, 
	migrate,
	csrf,
	mail,
	cache,
	api,
	jwt,
	marshmallow,
	sock,
)

def configuration_extensions(app):
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	login_manager.login_message = app.config['LOGIN_MESSAGE']
	babel.init_app(app, locale_selector=locale.get_locale)
	csrf.init_app(app)
	mail.init_app(app)
	cache.init_app(app)
	api.init_app(app)
	jwt.init_app(app)
	marshmallow.init_app(app)
	sock.init_app(app)




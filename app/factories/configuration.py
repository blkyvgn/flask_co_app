from app.vendors.utils.config import setup_configuration

def configuration_app(app, config_class):
	''' Add: STATIC_PATH_FOLDER
		UPLOAD_PATH_FOLDER
		BABEL_TRANSLATION_DIRECTORIES '''
	setup_configuration(app, config_class)
	app.config.from_object(config_class)
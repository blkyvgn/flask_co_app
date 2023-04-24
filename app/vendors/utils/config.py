from pathlib import Path

def setup_configuration(app, config_class=None):
	''' Collect configuration data '''

	setattr(config_class.__class__, 'STATIC_PATH_FOLDER', 
		str(Path(Path(app.root_path) / app._static_folder).resolve())
	)

	setattr(config_class.__class__, 'UPLOAD_PATH_FOLDER', 
		str(Path(Path(app.root_path) / app._static_folder / config_class.__class__.__dict__['UPLOAD_FOLDER']).resolve())
	)

	setattr(config_class.__class__, 'BABEL_TRANSLATION_DIRECTORIES', 
		str(Path(Path(app.root_path) / config_class.__class__.__dict__['TRANSLATION_DIRECTORY']).resolve())
	)

# def after_update_app_config_setup_configuration(app):
	# app.config['STATIC_PATH_FOLDER'] = str(Path(Path(app.root_path) / app._static_folder).resolve())
	# app.config['UPLOAD_PATH_FOLDER'] = str(
	# 	Path(Path(app.root_path) / app._static_folder).resolve() / app.config['UPLOAD_FOLDER']
	# )
	# app.config['BABEL_TRANSLATION_DIRECTORIES'] = str(
	# 	Path(Path(app.root_path) / app.config['TRANSLATION_DIRECTORY']).resolve()
	# )
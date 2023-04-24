import logging
from app.extensions import logger
import logging.handlers as handlers
from app.vendors.helpers.config import cfg 
from pathlib import Path
import time

def setup_logger(app, logger=logger):
	''' Configure Logging System '''

	# Log Levels
	log_levels = cfg('LOG_LEVELS')

	# Create log files if not exist
	log_directory = Path(app.root_path).resolve().parents[0] / cfg('LOG_DIR')
	log_files_paths = {}
	for log_level in log_levels:
		log_file_name = f'{log_level}.log'
		Path(log_directory / log_file_name).touch(exist_ok=True)
		log_files_paths[log_level] = Path(log_directory / log_file_name)

	# Set Logger Name
	logger.name = app.name + '.' + cfg('APP_NAME').replace(" ", "-")

	# Here we define our formatter
	formatter = logging.Formatter(cfg('LOG_FORMAT')) 

	if app.debug or app.testing:
		# Mode Check - Skip Debug And Test Mode.
		return 

	# Set info level on logger, which might be overwritten by handers. 
	# Suppress DEBUG messages.
	logger.setLevel(logging.INFO)

	if log_files_paths.get('info', False):
		info_log_handler = handlers.TimedRotatingFileHandler(
			log_files_paths['info'],
			when=cfg('LOG_TYPE_INTERVAL'), 
			interval=cfg('LOG_INTERVAL'), 
			backupCount=cfg('LOG_BACKUP_COUNT')
		)
		info_log_handler.setLevel(logging.INFO) 
		info_log_handler.setFormatter(formatter) 
		logger.addHandler(info_log_handler)

	if log_files_paths.get('warning', False):
		warning_log_handler = handlers.TimedRotatingFileHandler(
			log_files_paths['warning'],
			when=cfg('LOG_TYPE_INTERVAL'),
			interval=cfg('LOG_INTERVAL'),
			backupCount=cfg('LOG_BACKUP_COUNT')
		) 
		warning_log_handler.setLevel(logging.WARNING) 
		warning_log_handler.setFormatter(formatter) 
		logger.addHandler(warning_log_handler)

	if log_files_paths.get('error', False): 
		error_log_handler = handlers.TimedRotatingFileHandler(
			log_files_paths['error'],
			when=cfg('LOG_TYPE_INTERVAL'),
			interval=cfg('LOG_INTERVAL'),
			backupCount=cfg('LOG_BACKUP_COUNT')
		) 
		error_log_handler.setLevel(logging.ERROR) 
		error_log_handler.setFormatter(formatter) 
		logger.addHandler(error_log_handler)

	if log_files_paths.get('critical', False): 
		critical_log_handler = handlers.TimedRotatingFileHandler(
			log_files_paths['critical'], 
			when=cfg('LOG_TYPE_INTERVAL'),
			interval=cfg('LOG_INTERVAL'),
			backupCount=cfg('LOG_BACKUP_COUNT')
		) 
		critical_log_handler.setLevel(logging.CRITICAL) 
		critical_log_handler.setFormatter(formatter) 
		logger.addHandler(critical_log_handler)
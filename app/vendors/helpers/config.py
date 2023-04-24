from app.config import Configuration

def cfg(keys, config_class=Configuration):
	''' Get value from class Configuration 
		by chain of keys: cfg('PASSWD_LENGTH.MIN') '''
	keys_list = keys.split('.') 
	res = config_class.__dict__
	for key in keys_list:
		res = res.get(key, None)
		if res is None:
			break
	return res
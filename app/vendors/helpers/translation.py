from app.resources.translations import trs
from app.extensions import babel 
from flask import session, request, g
from app.vendors.helpers.config import cfg

def tr(key: None | str | list[str] = '__all__', lang=cfg('BABEL_DEFAULT_LOCALE')):
	''' return dict or str '''
	if key is None:
		return {}
	res = {}
	if key == '__all__':
		res = trs
	elif isinstance(key, list):
		keys = key.split(',')
		res = {k: v for k, v in trs.items() if k in keys}
	else:
		return trs.get(str(key), None)
	return res
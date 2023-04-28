from app.vendors.helpers.config import cfg
from collections import namedtuple

JinjaFilter = namedtuple('JinjaFilter', ['name', 'filter',])

def in_lang_or_default_filter(val, lang_key=None, default_key=cfg('BABEL_DEFAULT_LOCALE')):
	try:
		res = val.get(str(lang_key), val.get(default_key, None))
	except:
		res = None
	return res

def by_key_filter(val, key, default_key=None):
	try:
		res = val.get(str(key), val.get(default_key, None))
	except:
		res = None
	return res

def reverse_filter(val):
	return val[::-1]

def to_str_filter(val):
	return str(val)

def to_int_filter(val):
	return int(val)

def url_or_default_filter(val, default: str ='PLACEHOLDER'):
	default = cfg(f'DEFAULT_IMAGE.{default}')
	if val:
		url = '{0}/{1}'.format(cfg('UPLOAD_FOLDER'), val)
	else:
		url = default
	return url

jinja_filters = [
	JinjaFilter('in_lang_or_default', in_lang_or_default_filter),
	JinjaFilter('by_key', by_key_filter),
	JinjaFilter('revers', reverse_filter),
	JinjaFilter('to_str', to_str_filter),
	JinjaFilter('to_int', to_int_filter),
	JinjaFilter('url_or_default', url_or_default_filter),
]
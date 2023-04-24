from flask import g
from app.vendors.helpers.config import cfg


def get_json_by_lang(val, by_lang=None):
	key = g.current_language if by_lang is None else str(by_lang)
	dict_val = val
	lang_value = dict_val.get(key, None)
	return lang_value

def set_json_by_lang(val, v, by_lang=None):
	key = g.current_language if by_lang is None else str(by_lang)
	dict_val = {} if val is None else val.copy()
	dict_val[key] = v
	return dict_val
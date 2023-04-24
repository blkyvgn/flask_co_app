from flask import g, request
from app.vendors.helpers.config import cfg

def get_locale():
    lang = getattr(g, 'current_language', None)
    if lang is not None:
        lang = cfg('BABEL_DEFAULT_LOCALE')
    return lang

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
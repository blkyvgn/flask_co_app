from flask import Blueprint, request
from flask import render_template

bp_error = Blueprint('error', __name__)

@bp_error.app_errorhandler(400) 
def bad_request(error):
    desc='Bad Request'
    msg = f'{desc}:{error.description}'
    info = error.response 
    return render_template('error/400.html', msg=msg, info=info), 400

@bp_error.app_errorhandler(403) 
def forbidden_page(error):
    desc='Forbidden page'
    msg = f'{desc}:{error.description}'
    info = error.response 
    return render_template('error/403.html', msg=msg, info=info), 403

@bp_error.app_errorhandler(404) 
def not_found_error(error):
    desc='Page not found'
    msg = f'{desc}:{error.description}'
    info = error.response 
    return render_template('error/404.html', msg=msg, info=info), 404

@bp_error.app_errorhandler(405) 
def method_not_allowed(error):
    desc='Call wrong method'
    msg = f'{desc}:{error.description}'
    info = error.response 
    return render_template('error/405.html', msg=msg, info=info), 404

@bp_error.app_errorhandler(500) 
def internal_error(error):
    desc='Server error'
    msg = f'{desc}:{error.description}'
    info = error.response 
    return render_template('error/500.html', msg=msg, info=info), 500
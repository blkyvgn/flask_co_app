from flask import Blueprint
from app.factories import registration_blueprints
from .views.login import bp_login
from .views.register import bp_register

auth_blueprints = [
	bp_login,
	bp_register,
]

def bp_auth():
	bp_auth = Blueprint('auth', __name__, url_prefix='/<string:alias>/auth/')
	registration_blueprints(bp_auth, auth_blueprints)
	return bp_auth
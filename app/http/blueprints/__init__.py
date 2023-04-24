from .front.blueprint import bp_front
from .back.blueprint import bp_back
from .auth.blueprint import bp_auth
from .error.error import bp_error

front_bp = bp_front()
back_bp = bp_back()
auth_bp = bp_auth()

blueprints = [
	front_bp,
	back_bp,
	auth_bp,
	bp_error,
]
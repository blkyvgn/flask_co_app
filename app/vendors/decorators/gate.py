from functools import wraps
from flask import abort
from flask_login import current_user

__all__ = ('gate',)

def gate_decorator(): 
	def _gate():
		pass
	def allow(perms=[], abort_key=None):
		def gate_only(fn): 
			@wraps(fn)
			def wrapped(*args, **kwargs):
				if not current_user.is_anonymous:
					if None not in (abort_key, current_user) and not current_user.can(perms):
						return abort(abort_key) 
				return fn(*args, **kwargs)
			return wrapped 
		return gate_only

	def denie(perms=set(), abort_key=None): 
		def gate_denie(fn):
			@wraps(fn)
			def wrapped(*args, **kwargs):
				if not current_user.is_anonymous:
					if None not in (abort_key, current_user) and current_user.can(perms):
						return abort(abort_key) 
				return fn(*args, **kwargs)
			return wrapped 
		return gate_denie

	_gate.allow = allow 
	_gate.denie = denie 
	return _gate

gate = gate_decorator()
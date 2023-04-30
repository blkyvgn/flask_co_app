from flask import abort, g

__all__ = ('gate',)

def gate_utility(): 
	def _gate():
		pass
		
	def allow(perms=[], abort_key=403):
		if g.user.is_anonymous or not g.user.can_allow(perms):
			return abort(abort_key) 
			
	def deny(perms=[], abort_key=403): 
		if g.user.is_anonymous or not g.user.can_deny(perms):
			return abort(abort_key) 

	_gate.allow = allow 
	_gate.deny = deny
	return _gate

gate = gate_utility()
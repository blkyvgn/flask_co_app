from flask import g, redirect, url_for
from flask_login import current_user
from app.extensions import login_manager
from app.extensions import db


def auth_middleware(app):
	# Get Current Account
	from app.models import Account

	@login_manager.user_loader
	def load_user(userid):
		try:
			return db.get_or_404(Account, int(userid))
		except (TypeError, ValueError):
			return None
	
	@login_manager.unauthorized_handler
	def unauthorized():
		return redirect(url_for('auth.login.login', alias=g.company.alias))

	# Add Curent Account In Request Context
	@app.before_request
	def guser():
		g.user = current_user

	# Add Curent Account In Jinja2 Context (In Templates)
	@app.context_processor
	def inject_user():
		try:
			return { 'user': g.user }
		except AttributeError:
			return { 'user': None }

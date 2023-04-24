from flask import (Blueprint, render_template, redirect, url_for, request, flash, current_app,)
from app.vendors.helpers.url import is_safe_url
from app.vendors.helpers.mail import get_register_mail
from werkzeug.security import generate_password_hash
from flask_babel import lazy_gettext as _l
from app.vendors.helpers.config import cfg
from app.vendors.helpers.token import check_user_token
from flask_babel import _
from app.extensions import db
from flask_login import (
	login_user, 
	logout_user,
	current_user,
)
from app.http.blueprints.auth.forms import (
	LoginForm, 
	RegisterForm,
)
from app.events.auth import ( 
	signin_signal,
	signup_signal, 
	signout_signal, 
)
from app.services.celery.tasks import send_email
from app.models import Account

bp_login = Blueprint('login', __name__, url_prefix='/')


@bp_login.route('/login/', methods=['GET', 'POST'])
def login(alias):
	form = LoginForm()
	if form.validate_on_submit():
		''' After Login Form Validation '''
		curr_user = db.session.execute(
			db.select(Account).filter_by(email=form.email.data)
		).scalar()
		if curr_user is None or not curr_user.check_passwd(form.password.data):
			flash(_l(u'Invalid user email or password', category='warning'))
			return redirect(url_for('auth.login.login', alias=alias))

		signin_signal.send(current_app, username=curr_user.username)

		_next = request.args.get('next')
		if not is_safe_url(_next):
			return flask.abort(400)
	
		login_user(curr_user, remember=form.remember_me.data)
		return redirect(_next or url_for('back.dashboard.dashboard', alias=alias))

	return render_template('auth/login.html', 
		form = form
	)

@bp_login.route('/logout/', methods=['GET'])
def logout(alias):
	username = current_user.username
	logout_user()
	signout_signal.send(current_app, username=username)
	return redirect(url_for('front.home.home', alias=alias))

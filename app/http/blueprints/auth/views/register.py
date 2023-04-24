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

bp_register = Blueprint('register', __name__, url_prefix='/')

@bp_register.route('/register/', methods=['GET', 'POST'])
def register(alias):
	''' Sign in '''
	form = RegisterForm()
	if form.validate_on_submit():
		new_user = Account(
			username = form.username.data,
			email = form.email.data,
			password = generate_password_hash(form.password.data),
			is_activated = False,
		)
		new_user.save()

		try:
			# send_async_email.delay(email_data)
			email_data = get_register_mail(new_user, '/srv/mail/register.html')
			send_email.apply_async(
				args=[email_data], 
				countdown=60
			)
			flash(_l(u'Check your mail', category='success'))
			signup_signal.send(current_app, username=new_user.username)
		except:
			print('----------------------------------------------------')
			print(get_register_mail(new_user, '/srv/mail/register.html'))
			print('----------------------------------------------------')
			flash(_l(u'Email not sent', category='warning'))

		return redirect(url_for('front.home.home', alias=alias))
	return render_template('auth/register.html', 
		form = form
	)


@bp_register.route('/account_activate/<uidb64>/<token>/', methods=['GET'])
def account_activate(alias, uidb64, token):
	user = Account.get_by_uid(uidb64)
	# print(check_user_token(user, token))
	if user is not None and check_user_token(user, token):
		user.is_activated = True
		user.save()
		flash(_l(u'Account activated', category='success'))
		return redirect(url_for('auth.login.login', alias=alias))
	else:
		flash(_l(u'Activation error', category='warning'))
		return redirect('front.home.home', alias=alias)
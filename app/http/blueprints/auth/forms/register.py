from flask_wtf import FlaskForm
from app.vendors.helpers.config import cfg
from flask_babel import lazy_gettext as _l
from flask_babel import _
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)
from wtforms.validators import ( 
	ValidationError, 
	DataRequired, 
	Email, 
	EqualTo, 
	Length, 
)
from wtforms import ( 
	StringField, 
	PasswordField, 
	BooleanField, 
	SubmitField, 
)

__all__ = ('RegisterForm',)

class RegisterForm(FlaskForm):
	''' Register Form Class '''
	name = _(u'Registration form')

	username = StringField(
		label=(_(u'Username')),
		validators=[
			DataRequired(_(u'Field is required')), 
		])
	email = StringField(
		label=(_(u'Email')),
		validators=[
			DataRequired(_(u'Field is required')), 
		])
	password = PasswordField(
		label=(_(u'Password')),
		validators=[
			DataRequired(_(u'Field is required')), 
		])
	repeat_password = PasswordField(
		label=(_(u'Repeat Password')),
		validators=[
			DataRequired(_(u'Field is required')), 
			EqualTo('password', _(u'Passwords are not equal')),
		])
	
	submit = SubmitField(_(u'Sign In'))

	def validate_email(form, field):
		if not email_validation_check(field.data):
			error_message =  _(u'''Not valid email''')
			raise ValidationError(error_message)

	def validate_password(form, field):
		if not passwd_validation_check(field.data):
			error_message =  _(u'''Not valid password (a-zA-Z0-9!@#$%^&*)''')
			raise ValidationError(error_message)

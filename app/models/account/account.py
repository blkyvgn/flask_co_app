from app.vendors.helpers.mail import get_register_mail
from app.services.celery.tasks import send_email
from app.vendors.base.model import BaseModel
from flask_login import UserMixin
from flask import current_app
from app.extensions import db
from hashlib import md5
import base64
from werkzeug.security import (
	generate_password_hash, 
	check_password_hash,
)
from app.events.auth import ( 
	signin_signal,
	signup_signal, 
	signout_signal, 
)
from app.vendors.mixins.model import (
	ValidMixin,
	TimestampsMixin,
	MetaDataMixin,
	HelpersMixin,
	ImgMixin,
)


class Account(BaseModel, UserMixin, ValidMixin, HelpersMixin, TimestampsMixin): 
	__tablename__ = 'accounts'
	
	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	username = db.Column(
		db.String(120), 
		unique=True,
		nullable=False,
	) 
	email = db.Column(
		db.String(120), 
		unique=True, 
		nullable=False,
	) 
	password = db.Column(
		db.String(120), 
		unique=False, 
		nullable=False,
	)
	permissions = db.Column(
		db.JSON, 
		unique=False,
		default = list,
	)
	is_activated = db.Column(
		db.Boolean(1), 
		default=False, 
		nullable=True,
	)

	def __repr__(self):
		return f'Account: {self.username}'


	def set_passwd(self, password):
		''' Set User Password By MD5 '''
		self.password = generate_password_hash(password)

	def check_passwd(self, password):
		''' Check User Password '''
		return check_password_hash(self.password, password)

	def can_allow(self, perm_keys=[]):
		return set(perm_keys).issubset(set(self.permissions)):

	def can_deny(self, perm_keys=[]):
		return  len(set(perm_keys).intersection(set(self.permissions))) == 0:
		

	@classmethod
	def get_by_uid(cls, uidb64):
		try:
			uid = int(eval(base64.b64decode(uidb64))['uid'])
			user = db.session.execute(db.select(cls).filter_by(id=uid)).scalar_one()
		except:
			user = None
		return user

	def json(self):
		return {"id": self.id, "username": self.username}

	def send_register_mail(self):
		try:
			# send_async_email.delay(email_data)
			email_data = get_register_mail(self, '/srv/mail/register.html')
			send_email.apply_async(
				args=[email_data], 
				countdown=60
			)
			signup_signal.send(current_app, username=self.username)
		except:
			print('----------------------------------------------------')
			print(get_register_mail(self, '/srv/mail/register.html'))
			print('----------------------------------------------------')
			flash(_l(u'Email not sent', category='warning'))



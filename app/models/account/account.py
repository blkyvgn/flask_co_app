from flask_login import UserMixin
from app.vendors.base.model import BaseModel
from app.extensions import db
from hashlib import md5
import base64
from werkzeug.security import (
	generate_password_hash, 
	check_password_hash,
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

	def can(self, key='allow', perm_keys=[]):
		# ''' if all from list of permissions '''
		# can = set(self.permissions) <= set(perm_keys)
		# return can if key == 'allow' else not can
		if key == 'allow':
			''' if all from list of permissions '''
			return set(self.permissions) <= set(perm_keys)
		else:
			''' if one from list of permissions '''
			return  len(set(self.permissions) & set(perm_keys)) != 0
		

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


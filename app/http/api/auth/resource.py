from flask_restful import Resource, reqparse
from flask_babel import lazy_gettext as _l 
from werkzeug.security import (
	check_password_hash,
	generate_password_hash,
)
from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	get_jwt_identity,
	jwt_required,
	get_jwt,
)
from app.models import Account
from marshmallow import ValidationError
from .schemas import AccountSchema
from app.http.api.blacklist import BLACKLIST

USER_ALREADY_EXISTS = _l('A user with that username already exists.')
CREATED_SUCCESSFULLY = _l('User created successfully.')
USER_NOT_FOUND = _l('User not found.')
USER_DELETED = _l('User deleted.')
INVALID_CREDENTIALS = _l('Invalid credentials!')
USER_LOGGED_OUT = _l('User <id={pk}> successfully logged out.')
NOT_CONFIRMED_ERROR = (
	_l('You have not confirmed registration, please check your email.')
)
USER_CONFIRMED = _l('User confirmed.')

account_schema = AccountSchema()


class AccountRegisterResource(Resource):
	def post(self, alias: str):
		try:
			user_data = account_schema.load(request.get_json())
		except ValidationError as err:
			return err.messages, 400
		if Account.get_first_by_filter(username=user_data['username']):
			return {'message': 'A account with that username already exists.'}, 400
		account.save()
		return {'message': 'User created successfully.'}, 201


class AccountLoginResource(Resource):
	def post(self, alias: str):
		try:
			user_json = request.get_json()
			user_data = account_schema.load(user_json)
		except ValidationError as err:
			return err.messages, 400
		account = Account.get_first_by_filter(username=user_data['username'])
		if account and account.password == user_data['password']:
			if account.activated:
				access_token = create_access_token(identity=account.id, fresh=True)
				refresh_token = create_refresh_token(account.id)
				return {'access_token': access_token, 'refresh_token': refresh_token}, 200
			return {'message': NOT_CONFIRMED_ERROR}
		return {'message': 'Invalid credentials!'}, 401


class AccountLogoutResource(Resource):
	@jwt_required
	def post(self, alias: str):
		jti = get_jwt()['jti']
		pk = get_jwt_identity()
		BLACKLIST.add(jti)
		return {'message': 'User <id={}> successfully logged out.'.format(pk)}, 200


class TokenRefreshResource(Resource):
	@jwt_required(refresh=True)
	def post(self, alias: str):
		current_user = get_jwt_identity()
		new_token = create_access_token(identity=current_user, fresh=False)
		return {'access_token': new_token}, 200


class AccountConfirmResource(Resource):
	@classmethod
	def get(cls, alias: str, pk: int):
		account = Account.get_first_by_filter(id=pk)
		if not account:
			return {'message': USER_NOT_FOUND}, 404
		account.activated = True
		account.save()
		return {'message': USER_CONFIRMED}, 200

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

account_schema = AccountSchema()


class Account(Resource):
	@classmethod
	def get(cls, pk: int):
		account = Account.get_first_by_filter(id=pk)
		if not account:
			return {'message': 'User not found.'}, 404
		# return account.json(), 200

		return account_schema.dump(account), 200

	@classmethod
	def delete(cls, pk: int):
		account = UserModel.find_by_id(pk)
		if not account:
			return {'message': 'User not found.'}, 404
		account.delete()
		return {'message': 'User deleted.'}, 200



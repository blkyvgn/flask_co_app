from flask_restful import Resource
from flask_babel import lazy_gettext as _l 
from app.models import Account
from marshmallow import ValidationError
from .schemas import AccountSchema

account_schema = AccountSchema()

class AccountResource(Resource):
	@classmethod
	def get(cls, alias: str, pk: int):
		account = Account.get_first_by_filter(id=pk)
		if not account:
			return {'message': 'User not found.'}, 404
		# return account.json(), 200
		return account_schema.dump(account), 200

	@classmethod
	def delete(cls, alias: str, pk: int):
		account = Account.get_first_by_filter(id=pk)
		if not account:
			return {'message': 'User not found.'}, 404
		account.delete()
		return {'message': 'User deleted.'}, 200



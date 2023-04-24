from marshmallow import Schema, fields
from app.extensions import marshmallow as mm
from app.models import Account


class AccountSchema(mm.SQLAlchemyAutoSchema):
	class Meta:
		model = Account
		load_only = ('password',)
		dump_only = ('id', 'is_activated')
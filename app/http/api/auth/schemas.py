from marshmallow import Schema, fields
from app.extensions import marshmallow as mm
from app.models import Account


class AccountSchema(mm.SQLAlchemyAutoSchema):
	class Meta:
		model = Account
	
	username = mm.auto_field()
	email = mm.auto_field()
	password = mm.auto_field()
from marshmallow import Schema, fields
from app.extensions import marshmallow as mm
from app.models import Category


class CategorySchema(mm.SQLAlchemyAutoSchema):
	class Meta:
		model = Category
		# load_only = ('name',)
		dump_only = ('id',)
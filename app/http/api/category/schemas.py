from marshmallow import Schema, fields
from app.extensions import marshmallow as mm
from marshmallow_sqlalchemy.fields import Nested
from app.models import Category


class ParentCategorySchema(mm.SQLAlchemySchema):
	class Meta:
		model = Category
		load_instance = True

	id = mm.auto_field()
	_name = mm.auto_field()

class ChildCategorySchema(mm.SQLAlchemySchema):
	class Meta:
		model = Category
		load_instance = True

	id = mm.auto_field()
	_name = mm.auto_field()

class CategorySchema(mm.SQLAlchemySchema):
	class Meta:
		model = Category
		load_instance = True

	id = mm.auto_field()
	_name = mm.auto_field()
	_short_desc = mm.auto_field()
	thumb = mm.auto_field()
	# parent = mm.auto_field()
	created_at = mm.auto_field()
	parent = Nested(ParentCategorySchema)
	children = Nested(ChildCategorySchema, many=True)

from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage

from flask_restful import Resource
from .schemas import CategorySchema
from app.models import Category

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)

class CategoryResource(Resource):
	@classmethod
	def get(cls, alias: str, pk: int):
		category = Category.get_first_by_filter(id=pk)
		if category:
			return category_schema.dump(category), 200
		return {'message': 'Category not found'}, 404

class CategoryListResource(Resource):
	@classmethod
	def get(cls, alias: str):
		categories = Category.get_all(is_valid=True)
		return {'categories': category_list_schema.dump(categories)}, 200
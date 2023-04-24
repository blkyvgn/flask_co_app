from flask_restful import Resource
from .schemas import (
	ArticleSchema,
	ArticleBodySchema,
)
from app.models import (
	Article, 
	ArticleBody,
)

article_schema = ArticleSchema()
article_list_schema = ArticleSchema(many=True)
article_body_list_schema = ArticleBodySchema(many=True)

class ArticleResource(Resource):
	@classmethod
	def get(cls, alias: str, pk: int):
		article = Article.get_first_by_filter(id=pk)
		if article:
			return article_schema.dump(article), 200

		return {'message': 'Article not found'}, 404

class ArticleListResource(Resource):
	@classmethod
	def get(cls, alias: str):
		articles = Article.get_all(is_valid=True)
		return {'articles': article_list_schema.dump(articles)}, 200
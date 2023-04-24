from marshmallow import Schema, fields
from app.extensions import marshmallow as mm
from app.models import (
	Article, 
	ArticleBody,
)


class ArticleBodySchema(mm.SQLAlchemyAutoSchema):
	class Meta:
		model = ArticleBody
		# load_only = ('lang', 'body')
		dump_only = ('id',)

class ArticleSchema(mm.SQLAlchemyAutoSchema):
	class Meta:
		model = Article
		# load_only = ('name', 'bodies')
		dump_only = ('id',)

	bodies = mm.Nested(ArticleBodySchema(many=True))
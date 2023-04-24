from app.vendors.base.model import BaseModel
from app.extensions import db
from app.vendors.mixins.model import (
	ValidMixin,
	TimestampsMixin,
)
from sqlalchemy.orm import relationship



class Comment(BaseModel): 
	__tablename__ = 'comments'
	
	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	username = db.Column(
		db.String(120),
		nullable=False,
	) 
	text = db.Column(
		db.Text, 
		unique=False, 
		nullable=False,
	)
	article_id = db.Column(
		db.Integer, 
		db.ForeignKey('articles.id'),
	)
	article = relationship(
		'Article', 
		back_populates='comments',
	)

	def __repr__(self):
		return f'Comment: {self.id}'
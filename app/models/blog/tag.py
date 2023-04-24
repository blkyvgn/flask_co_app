from app.vendors.base.model import BaseModel
from app.extensions import db
from app.vendors.mixins.model import (
	ValidMixin,
	TimestampsMixin,
)


class Tag(BaseModel):
	__tablename__ = 'tags'

	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	tag = db.Column(
		db.String(50),
		unique=False, 
		nullable=False,
	)
	type_id = db.Column(
		db.Integer,
		unique=False, 
		nullable=False,
	)
	type_key = db.Column(
		db.String(50),
		unique=False, 
		nullable=False,
	)

	def __repr__(self):
		return f'Tag: {self.tag}'

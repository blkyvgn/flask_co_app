from flask import g
from app.extensions import db
from app.vendors.base.model import BaseModel
from app.vendors.helpers.config import cfg
from app.vendors.helpers.model import (
	get_json_by_lang,
	set_json_by_lang,
)
from sqlalchemy.orm import (
	relationship, 
	backref,
)
from sqlalchemy import (
	func, 
	desc,
)
from app.vendors.mixins.model import (
	ValidMixin,
	TimestampsMixin,
	MetaDataMixin,
	HelpersMixin,
	ImgMixin,
)


class Category(BaseModel, ValidMixin, TimestampsMixin, HelpersMixin, ImgMixin): 
	__tablename__ = 'categories'
	
	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	_name = db.Column('name',
		db.JSON, 
		unique=False,
		nullable=False,
		default=dict
	) 
	_short_desc = db.Column('short_desc',
		db.JSON, 
		unique=False, 
		default=dict,
	)
	thumb = db.Column(
		db.String(255),
		unique=False,
		nullable=True,
	)
	parent_id = db.Column(
		db.Integer, 
		db.ForeignKey('categories.id'),
		nullable=True,
	)
	art_count = db.Column(
		db.Integer(),
		unique=False, 
		nullable=True,
	)
	children = relationship(
		'Category', 
		backref=backref('parent', remote_side=[id])
	)
	articles = relationship(
		'Article', 
		back_populates='category'
	)
	company_id = db.Column(
		db.Integer, 
		db.ForeignKey('companies.id'),
		nullable=True,
	)
	company = relationship(
		'Company', 
		back_populates='categories'
	)

	def __repr__(self):
		return f'Category: {self.name}'

	@property
	def name(self):
		return get_json_by_lang(self._name)

	@name.setter
	def name(self, v):
		self._name = set_json_by_lang(self._name, v)

	@property
	def short_desc(self):
		return get_json_by_lang(self._short_desc)

	@short_desc.setter
	def short_desc(self, v):
		self._short_desc = set_json_by_lang(self._short_desc, v)

	# helpers
	@classmethod
	def get_category_form_choices(clx, with_empty=True):
		categories = db.session.execute(
			db.select(clx).order_by(desc('created_at'))
		).scalars().all()
		if with_empty:
			return [('', '---'), *[(cat.id, cat.name) for cat in categories]]
		return [(cat.id, cat.name) for cat in categories]



from flask import g
from app.extensions import db, cache
from sqlalchemy.orm import relationship
from app.vendors.helpers.config import cfg
from app.vendors.base.model import BaseModel
from app.vendors.mixins.model import (
	ValidMixin,
	TimestampsMixin,
	MetaDataMixin,
	HelpersMixin,
	ImgMixin,
)
from sqlalchemy import (
	func, 
	desc,
)


class Company(BaseModel, ValidMixin, TimestampsMixin, HelpersMixin, ImgMixin): 
	__tablename__ = 'companies'
	
	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	alias = db.Column(
		db.String(80),
		unique=True,
		nullable=False,
	)
	_name = db.Column('name',
		db.JSON, 
		unique=False,
		default = dict,
	) 
	logo = db.Column(
		db.String(255),
		unique=False,
		nullable=True,
	)
	options = db.Column(
		db.JSON, 
		unique=False,
		default = dict,
	)
	articles = relationship(
		'Article', 
		back_populates='company'
	)
	categories = relationship(
		'Category', 
		back_populates='company'
	)
	def __repr__(self):
		return f'Company:{self.name}'

	@property
	def name(self):
		return get_json_by_lang(self._name)

	@name.setter
	def name(self, v):
		self._name = set_json_by_lang(self._name, v)

	def save(self):
		cache.delete_memoized(Company.get_from_cache, Company, self.alias)
		super().save()

	def destroy(self):
		cache.delete_memoized(Company.get_from_cache, Company, self.alias)
		super().destroy()

	@classmethod
	@cache.memoize(cfg('CACHE_TIMEOUT.YEAR'))
	def get_from_cache(cls, alias):
		company = db.session.execute(
			db.select(cls).filter_by(alias=alias)
		).scalar()
		return company

from flask import g
from pathlib import Path
from app.extensions import db
from sqlalchemy.orm import relationship
from app.vendors.helpers.config import cfg
from app.vendors.base.model import BaseModel
from app.vendors.helpers.model import (
	get_json_by_lang,
	set_json_by_lang,
)
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


class Article(BaseModel, ValidMixin, TimestampsMixin, HelpersMixin, ImgMixin): 
	__tablename__ = 'articles'
	
	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	_name = db.Column('name',
		db.JSON, 
		unique=False,
		default=dict,
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
	bodies = relationship(
		'ArticleBody', 
		back_populates='article'
	)
	views = db.Column(
		db.Integer(),
		unique=False, 
		nullable=True,
	)
	comm_count = db.Column(
		db.Integer(),
		unique=False, 
		nullable=True,
	)
	comments = relationship(
		'Comment', 
		back_populates='article'
	)
	category_id = db.Column(
		db.Integer, 
		db.ForeignKey('categories.id')
	)
	category = relationship(
		'Category', 
		back_populates='articles'
	)
	company_id = db.Column(
		db.Integer, 
		db.ForeignKey('companies.id'),
		nullable=True,
	)
	company = relationship(
		'Company', 
		back_populates='articles'
	)
		
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


	def __repr__(self):
		return f'Article: {self.name}'


	@staticmethod
	def upload_body_image(image_file, 
			file_allowed_exts = cfg('ALLOWED_IMAGE_EXTENSIONS'), 
			ext_path = '',
			file_name = ''
		):
		''' image_file: form.<image_name>.data or request.files[<image_name>] ''' 
		if image_file.filename == '':
			return None
		file_ext = image_file.filename.split('.')[-1]
		if file_ext not in file_allowed_exts:
			return None
		try:
			dir_path = Path(cfg('UPLOAD_PATH_FOLDER')) / ext_path
			filename = image_file.filename if not file_name else f'{file_name}.{file_ext}'
			img_path = dir_path / filename
			image_file.save(img_path)
			file_ext_path = str(Path(ext_path) / filename)
			upload_folder = cfg('UPLOAD_FOLDER')
			# return f'{request.url_root}public/{upload_folder}/{file_ext_path}'
			return f'/{upload_folder}/{file_ext_path}'
		except:
			return None



class ArticleBody(BaseModel, MetaDataMixin):
	__tablename__ = 'article_bodies'

	id = db.Column(
		db.Integer, 
		primary_key=True
	)
	lang = db.Column(
		db.String(10), 
		unique=False,
		nullable=False,
	) 
	body = db.Column(
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
		back_populates='bodies',
	)
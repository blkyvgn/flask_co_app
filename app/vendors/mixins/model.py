from flask import (current_app, request, g,)
from app.extensions import db
from datetime import datetime
from app.extensions import logger
from app.vendors.helpers.config import cfg
from app.vendors.helpers.image import resize_image
from pathlib import Path


class ValidMixin:
	is_valid = db.Column(
		db.Boolean(0), 
		default=False, 
		nullable=True,
	) 

class TimestampsMixin:
	created_at = db.Column(
		db.DateTime, 
		default=datetime.utcnow, 
		nullable=True,
	) 
	updated_at = db.Column(
		db.DateTime, 
		onupdate=datetime.utcnow, 
		nullable=True,
	)

class MetaDataMixin:
	meta_keywords = db.Column(
		db.String(255),
		unique=False,
		nullable=True,
	)
	meta_description = db.Column(
		db.String(255),
		unique=False,
		nullable=True,
	)
	meta_author = db.Column(
		db.String(255),
		unique=False,
		nullable=True,
	)

class HelpersMixin:
	def name_in_lang_or_default(self, lang_key=None, default_key=cfg('BABEL_DEFAULT_LOCALE')):
		try:
			name = self.name.get(str(lang_key), self.name.get(default_key, None))
		except:
			name = None
		return name

	@classmethod
	def get_first_by_filter(cls, _or=False, **kwargs) -> 'BaseModel':
		if not _or:
			item_select = db.select(cls).filter_by(**kwargs)
		else:
			filters = [getattr(cls, k) == v for k, v in kwargs.items()]
			item_select = db.select(cls).filter(or_(False, *filters))
		item = db.session.execute(item_select).scalar()
		return item


class ImgMixin:
	def save_img(self, img, ext_path='', file_name='', file_allowed_exts=cfg('ALLOWED_IMAGE_EXTENSIONS'), width=None):
		if img.filename == '':
			return None
		file_ext = img.filename.split('.')[-1]
		if file_ext not in file_allowed_exts:
			return None
			
		try:
			img_path = Path(cfg('UPLOAD_PATH_FOLDER')) / ext_path
			filename = img.filename if not file_name else f'{file_name}.{file_ext}'
			img_path = img_path / filename
			img.save(img_path)
			if width and isinstance(width, int):
				new_img = resize_image(img_path, width)
				new_img.save(img_path)
			return str(Path(ext_path) / filename)
		except:
			return None

	def img_url_or_default(self, img_name, default=cfg('DEFAULT_IMAGE.PLACEHOLDER')):
		img = getattr(self, img_name)
		try:
			url = '{0}/{1}'.format(cfg('UPLOAD_FOLDER'), img)
		except:
			url = default
		return url
	
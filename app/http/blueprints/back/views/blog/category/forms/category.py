from flask_wtf import FlaskForm
from app.vendors.helpers.config import cfg
from flask_babel import lazy_gettext as _l 
from flask_babel import _
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)
from wtforms.validators import ( 
	ValidationError, 
	DataRequired, 
	Email, 
	Length, 
)
from wtforms import ( 
	StringField, 
	TextAreaField,
	FileField,
	BooleanField, 
	SelectField,
	SubmitField, 
)


class CategoryForm(FlaskForm):
	name = StringField(_(u'Name'),
		validators=[
			DataRequired(_(u'Field is required')), 
		])
	short_desc = TextAreaField(_(u'Short description'))
	thumb = FileField(_(u'Thumbnail'))
	is_valid = BooleanField(_(u'Valid'))
	parent_id = SelectField(_(u'Parent'))

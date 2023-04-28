from flask import (Blueprint, render_template, redirect, url_for, request, flash, g,)
from app.vendors.helpers.pagination import get_current_page
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_required
from app.vendors.helpers.config import cfg
from flask_babel import lazy_gettext as _l
from flask_babel import _
from app.extensions import logger
from app.extensions import db
from app.vendors.utils.gate import gate
from app.vendors.helpers.model import (
	get_json_by_lang,
	set_json_by_lang,
)
from app.http.blueprints.back.views.blog.category.forms.category import (
    CategoryForm,
)
from sqlalchemy import (
	func, 
	desc,
)
from app.models import (
	Category,
	Article,
)

bp_adm_cat = Blueprint('cat', __name__, url_prefix='/')

@bp_adm_cat.route('/category/list/', methods=['GET']) 
@login_required
def category_list(alias):
	gate.allow(['access_admin_pages'], 403)
	select_categories = db.select(
			Category
		).\
		filter_by(company_id=g.company.id).\
		order_by(desc('created_at'))
	pagination_categories = db.paginate(select_categories,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('back/category/index.html',
		pagination_categories = pagination_categories,
	)


@bp_adm_cat.route('/category/create/', methods=['GET']) 
@login_required
def category_create(alias):
	gate.allow(['access_admin_pages'], 403)
	form = CategoryForm()
	form.parent_id.choices = Category.get_category_form_choices()
	return render_template('back/category/create.html', 
		form = form,
	)


@bp_adm_cat.route('/category/store/', methods=['POST']) 
@login_required
def category_store(alias):
	gate.allow(['access_admin_pages'], 403)
	form = CategoryForm()
	form.parent_id.choices = Category.get_category_form_choices()
	if form.validate_on_submit():
		thumb = None
		category = Category(
			name = form.name.data,
			short_desc = form.short_desc.data,
			is_valid = form.is_valid.data,
			parent_id = form.parent_id.data,
			company_id = g.company.id,
		)
		if form.thumb.data:
			thumb = category.save_img(form.thumb.data, width=cfg('IMAGE_WIDTH.SHOWCASE'))
		category.thumb = thumb
		if not category.save():
			flash(_l(u'Category not saved', category='warning'))
		return redirect(url_for('back.cat.category_list', alias=alias))
	return render_template('back/category/create.html', 
		form = form
	)


@bp_adm_cat.route('/category/<int:cat_id>/show', methods=['GET']) 
@login_required
def category_show(alias, cat_id):
	gate.allow(['access_admin_pages'], 403)
	select_category = db.select(
			Category, 
			func.count(Article.id).label('articles_count')
		).\
		filter_by(id=cat_id).\
		outerjoin(Category.articles)
	try:
		category = db.session.execute(select_category).one()
	except NoResultFound as e:
		return abort(404)
	return render_template('back/category/item.html',
		category = category,
	)


@bp_adm_cat.route('/category/<int:cat_id>/edit/', methods=['GET']) 
@login_required
def category_edit(alias, cat_id):
	gate.allow(['access_admin_pages'], 403)
	category = db.get_or_404(Category, int(cat_id))
	form = CategoryForm(obj=category)
	form.parent_id.choices = Category.get_category_form_choices()
	return render_template('back/category/edit.html',
		category = category,
		form = form,
	)


@bp_adm_cat.route('/category/<int:cat_id>/update/', methods=['POST']) 
@login_required
def category_update(alias, cat_id):
	gate.allow(['access_admin_pages'], 403)
	category = db.get_or_404(Category, int(cat_id))
	form = CategoryForm(obj=category)
	form.parent_id.choices = Category.get_category_form_choices()
	if form.validate_on_submit():
		thumb = None
		category.name = form.name.data
		category.short_desc = form.short_desc.data
		category.is_valid = form.is_valid.data
		category.parent_id = form.parent_id.data
		if form.thumb.data:
			thumb = category.save_img(form.thumb.data, width=cfg('IMAGE_WIDTH.THUMBNAIL'))
		category.thumb = thumb
		if not category.save():
			flash(_l(u'Category not saved', category='warning'))
		return redirect(url_for('back.cat.category_list', alias=alias))
	return render_template('back/category/edit.html',
		category = category,
		form = form
	)


@bp_adm_cat.route('/category/<int:cat_id>/destroy/', methods=['GET']) 
@login_required
def category_destroy(alias, cat_id):
	gate.allow(['access_admin_pages'], 403)
	category = db.get_or_404(Category, int(cat_id))
	category.destroy()
	return redirect(url_for('back.cat.category_list', alias=alias))
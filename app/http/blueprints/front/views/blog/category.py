from flask import Blueprint, render_template, request, session, g, abort
from app.vendors.helpers.pagination import get_current_page
from sqlalchemy.orm.exc import NoResultFound
from flask_babel import lazy_gettext as _l
from app.vendors.helpers.config import cfg
from app.extensions import db
from sqlalchemy import (
	func, 
	desc,
)
from app.models import (
	Category,
	Article,
)

bp_cat = Blueprint('cat', __name__, url_prefix='/blog/')


@bp_cat.route('/category/list/', methods=['GET']) 
def category_list(alias):
	select_categories = db.select(
			Category, 
		).\
		filter_by(is_valid=True).\
		filter_by(company_id=g.company.id).\
		order_by(desc('created_at'))
	pagination_categories = db.paginate(select_categories,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('front/blog/category/list.html',
		pagination_categories = pagination_categories,
	)



@bp_cat.route('/category/<int:cat_id>/articles/', methods=['GET']) 
def category_articles(alias, cat_id):
	select_category = db.select(
			Category, 
			func.count(Article.id).label('articles_count')
		).\
		filter_by(id=int(cat_id)).\
		filter_by(is_valid=True).\
		filter_by(company_id=g.company.id).\
		outerjoin(Category.articles)
	try:
		category = db.session.execute(select_category).one()
	except NoResultFound as e:
		return abort(404)

	select_articles = db.select(
			Article
		).\
		filter_by(category_id=int(cat_id)).\
		filter_by(is_valid=True).\
		order_by(desc('created_at'))
	pagination_articles = db.paginate(select_articles,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('front/blog/category/articles.html',
		category = category,
		pagination_articles = pagination_articles,
	)
from flask import (Blueprint, render_template, request, session, g, abort)
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
	ArticleBody,
	Comment,
)

bp_art = Blueprint('art', __name__, url_prefix='/blog/')


@bp_art.route('/article/list/', methods=['GET']) 
def article_list(alias):
	select_articles = db.select(
			Article,
		).\
		filter_by(is_valid=True).\
		filter_by(company_id=g.company.id).\
		order_by(desc('created_at'))
	pagination_articles = db.paginate(select_articles,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('front/blog/article/list.html',
		pagination_articles = pagination_articles,
	)

@bp_art.route('/article/<int:art_id>/item/', methods=['GET']) 
def article_item(alias, art_id):
	# article_select = db.select(
	# 		Article, ArticleBody.body
	# 	).\
	# 	filter_by(id=int(art_id)).\
	# 	filter_by(is_valid=True).\
	# 	outerjoin(Article.bodies).\
	# 	filter_by(lang=g.current_language)
	# try:
	# 	article = db.session.execute(article_select).one()
	# except NoResultFound as e:
	# 	return abort(404)

	article_select = db.select(
			Article,
		).\
		filter_by(id=int(art_id)).\
		filter_by(is_valid=True)
	article = db.session.execute(article_select).scalar()
	if article is None:
		return abort(404)
	
	body_select = db.select(
			ArticleBody
		).\
		filter_by(article_id=article.id).\
		filter_by(lang=g.current_language)
	article_body = db.session.execute(body_select).scalar()

	select_category = db.select(Category).\
		filter_by(id=int(article.category_id)).\
		filter_by(is_valid=True).\
		filter_by(company_id=g.company.id)
	category = db.session.execute(select_category).scalar()
	if category is None:
		return abort(404)
	
	return render_template('front/blog/article/item.html',
		category = category,
		article = article,
		article_body = article_body,
	)
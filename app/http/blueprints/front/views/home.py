from flask import Blueprint, render_template, abort, request, g
from app.vendors.helpers.translation import tr
from app.vendors.helpers.config import cfg
from app.extensions import db, cache
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

bp_home = Blueprint('home', __name__, url_prefix='/')


@bp_home.route('/home', methods=['GET'])
# @cache.cached(timeout=cfg('CACHE_TIMEOUT.DAY'))
def home(alias):
	# print(tr('article', lang=g.current_language))
	select_articles = db.select(
			Article,
			func.count(Comment.id).label('comments_count')
		).\
		filter_by(is_valid=True).\
		filter_by(company_id=g.company.id).\
		outerjoin(Article.comments).\
		group_by(Article.id).\
		order_by(desc('views')).\
		limit(5)
	articles = db.session.execute(select_articles).all()
	return render_template('front/home.html',
		articles = articles,
	)

@bp_home.route('/contact', methods=['GET'])
def contact(alias):
	return render_template('front/contact.html')

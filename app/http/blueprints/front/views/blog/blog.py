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

bp_blog = Blueprint('blog', __name__, url_prefix='/blog/')

@bp_blog.route('/blog', methods=['GET']) 
def blog(alias):
	select_categories = db.select(
			Category, 
			func.count(Article.id).label('articles_count')
		).\
		filter_by(is_valid=True).\
		filter_by(company_id=g.company.id).\
		outerjoin(Category.articles).\
		group_by(Category.id).\
		order_by(desc('articles_count')).\
		limit(cfg('NUMBER_PER_PAGE'))
	categories = db.session.execute(select_categories).all()

	select_articles = db.select(
			Article,
			func.count(Comment.id).label('comments_count')
		).\
		filter_by(is_valid=True).\
		filter_by(company_id=g.company.id).\
		outerjoin(Article.comments).\
		group_by(Article.id).\
		order_by(desc('views')).\
		limit(cfg('NUMBER_PER_PAGE'))
	articles = db.session.execute(select_articles).all()

	return render_template('front/blog/blog.html',
		categories = categories,
		articles = articles,
	)

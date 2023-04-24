from flask import (Blueprint, render_template, redirect, url_for, request, flash, g, abort,)
from app.vendors.helpers.pagination import get_current_page
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_required
from app.vendors.helpers.config import cfg
from app.extensions import logger
from app.extensions import db
from app.vendors.utils.gate import gate
from app.vendors.helpers.model import (
	get_json_by_lang,
	set_json_by_lang,
)
from sqlalchemy import (
	func, 
	desc,
)
from app.models import (
	Category,
	Article,
	ArticleBody,
)

bp_adm_art = Blueprint('art', __name__, url_prefix='/')

@bp_adm_art.route('/article/list/', methods=['GET']) 
@login_required
def article_list(alias):
	gate.allow(['access_admin_pages'], 403)
	select_articles = db.select(Article).order_by(desc('created_at'))
	pagination_articles = db.paginate(select_articles,
		page=get_current_page(request), 
		per_page=cfg('NUMBER_PER_PAGE'), 
		max_per_page=cfg('MAX_PER_PAGE')
	)
	return render_template('back/article/index.html',
		pagination_articles = pagination_articles,
	)


@bp_adm_art.route('/article/create/', methods=['GET']) 
@login_required
def article_create(alias):
	gate.allow(['access_admin_pages'], 403)
	categories = Category.get_category_form_choices(with_empty=False)
	return render_template('back/article/create.html',
		categories = categories,
	)


@bp_adm_art.route('/article/store/', methods=['POST']) 
@login_required
def article_store(alias):
	gate.allow(['access_admin_pages'], 403)
	categories = Category.get_category_form_choices(with_empty=False)
	if request.validate.post({
			'name': 'required|min:4',
			'short_desc': 'required|min:10|max:200',
			'body': 'required',
		}):
		thumb = None
		is_valid = True if request.form.get('is_valid') == 'on' else False
		article = Article(
			name = request.form.get('name', ''),
			short_desc = request.form.get('short_desc', ''),
			is_valid = is_valid,
			category_id = request.form.get('category_id'),
			company_id = g.company.id
		)
		if 'thumb' in request.files and request.files['thumb'].filename != '':
			thumb = article.save_img(request.files['thumb'], width=cfg('IMAGE_WIDTH.THUMBNAIL'))
		article.thumb = thumb
		article.bodies.append(
			ArticleBody(
				lang=g.current_language, 
				body=request.form.get('body', '')
			)
		)
		article.save()
		return redirect(url_for('back.art.article_list', alias=alias))
	return render_template('back/article/create.html',
		categories = categories,
	)


@bp_adm_art.route('/article/<int:art_id>/show', methods=['GET']) 
@login_required
def article_show(alias, art_id):
	gate.allow(['access_admin_pages'], 403)
	article_select = db.select(
			Article, ArticleBody.body
		).\
		filter_by(id=int(art_id)).\
		outerjoin(Article.bodies).\
		filter_by(lang=g.current_language)
	try:
		article = db.session.execute(article_select).one()
	except NoResultFound as e:
		return abort(404)

	return render_template('back/article/item.html',
		article = article,
	)


@bp_adm_art.route('/article/<int:art_id>/edit/', methods=['GET']) 
@login_required
def article_edit(alias, art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(Article, int(art_id))
	body_select = db.select(
			ArticleBody
		).\
		filter_by(article_id=article.id).\
		filter_by(lang=g.current_language)
	article_body = db.session.execute(body_select).scalar()
	body = article_body.body if article_body else ''
	setattr(article, 'body', body)
	categories = Category.get_category_form_choices(with_empty=False)
	return render_template('back/article/edit.html',
		article = article,
		article_body = article_body,
		categories = categories,
	)


@bp_adm_art.route('/article/<int:art_id>/update/', methods=['POST']) 
@login_required
def article_update(alias, art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(Article, int(art_id))
	categories = Category.get_category_form_choices(with_empty=False)
	if request.validate.post({
			'name': 'required|min:4',
			'short_desc': 'required|min:10|max:200',
		}):
		thumb = None
		is_valid = True if request.form.get('is_valid') == 'on' else False
		article.name = request.form.get('name', '')
		article.short_desc = request.form.get('short_desc', '')
		article.is_valid = is_valid
		article.category_id = request.form.get('category_id')
		if 'thumb' in request.files and request.files['thumb'].filename != '':
			thumb = article.save_img(request.files['thumb'], width=cfg('IMAGE_WIDTH.THUMBNAIL'))
		article.thumb = thumb
		article.save()
		body_select = db.select(
				ArticleBody
			).\
			filter_by(article_id=article.id).\
			filter_by(lang=g.current_language)
		article_body = db.session.execute(body_select).scalar()
		if article_body:
			article_body.body = request.form.get('body', '')
			article_body.lang = g.current_language
			article_body.save()
		else:
			article.bodies.append(
				ArticleBody(
					lang=g.current_language, 
					body=request.form.get('body', '')
				)
			)
		return redirect(url_for('back.art.article_list', alias=alias))
	return render_template('back/article/edit.html',
		article = article,
		categories = categories,
	)


@bp_adm_art.route('/article/<int:art_id>/destroy/', methods=['GET']) 
@login_required
def article_destroy(alias, art_id):
	gate.allow(['access_admin_pages'], 403)
	article = db.get_or_404(Article, int(art_id))
	article.destroy()
	return redirect(url_for('back.art.article_list', alias=alias))

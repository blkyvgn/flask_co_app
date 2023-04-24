from flask import Blueprint, redirect, session, jsonify, g, request
from app.extensions import db, cache
from app.vendors.helpers.config import cfg

bp_serv = Blueprint('serv', __name__, url_prefix='/')



@bp_serv.route('/change-locale/<lang>/', methods=['GET'])
def change_locale(alias, lang):
	session['current_language'] = lang
	return redirect(request.referrer)


@bp_serv.route('/options/', methods=['POST']) 
def options(alias):
	return jsonify({'success':'Stub: change application settings'})


@bp_serv.route('/search/', methods=['POST'])
def search(alias):
	session.pop('search_name', default=None)
	if search_value := request.form.get('search_name', None):
		session['search_name'] = search_value
		# g.search = search_value
	return redirect(request.referrer)


from app.models import Article
@bp_serv.route('/upload-article-image/', methods=['POST']) 
def article_image_upload(alias):
	image_path = Article.upload_body_image(request.files['image'])
	return jsonify({'img':image_path})
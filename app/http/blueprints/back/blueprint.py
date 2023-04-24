from flask import Blueprint, render_template, abort
from app.factories import registration_blueprints
from .views.dashboard import bp_dashboard
from .views.blog.category.category import bp_adm_cat
from .views.blog.article.article import bp_adm_art


back_blueprints = [
	bp_dashboard,
	bp_adm_cat,
	bp_adm_art,
]

def bp_back():
	bp_back = Blueprint('back', __name__, url_prefix='/<string:alias>/')
	registration_blueprints(bp_back, back_blueprints)
	return bp_back
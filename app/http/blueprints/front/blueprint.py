from flask import Blueprint
from app.factories import registration_blueprints
from .views.home import bp_home
from .views.serv import bp_serv
from .views.blog.blog import bp_blog
from .views.blog.article import bp_art
from .views.blog.category import bp_cat

front_blueprints = [
	bp_home,
	bp_serv,
	bp_blog,
	bp_art,
	bp_cat,
]

def bp_front():
	bp_front = Blueprint('front', __name__, url_prefix='/<string:alias>/')
	registration_blueprints(bp_front, front_blueprints)
	return bp_front
from flask import Blueprint, render_template, abort, request
from app.extensions import db, cache
from app.vendors.helpers.config import cfg

bp_home = Blueprint('home', __name__, url_prefix='/')


@bp_home.route('/home', methods=['GET'])
# @cache.cached(timeout=cfg('CACHE_TIMEOUT.DAY'))
def home(alias):
	return render_template('front/home.html')

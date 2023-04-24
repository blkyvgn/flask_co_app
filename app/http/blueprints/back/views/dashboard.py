from flask import Blueprint, render_template, abort, request
from flask_login import login_required

bp_dashboard = Blueprint('dashboard', __name__, url_prefix='/')

@bp_dashboard.route('/dashboard')
@login_required
def dashboard(alias):
	return render_template('back/dashboard.html')
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
import json

bp_chat = Blueprint('chat', __name__, url_prefix='/chat/')

@bp_chat.route('/list', methods=['GET']) 
def chat(alias):
	rooms = [{'id':1, 'name':'common'}]
	return render_template('front/chat/index.html',
		rooms = rooms
	)

@bp_chat.route('/room/<int:pk>/', methods=['GET']) 
def room(alias, pk):
	room = {'id':pk, 'name':'common'}
	users = [
		{'id':1, 'username':'qqq'},
		{'id':2, 'username':'www'},
	]
	return render_template('front/chat/room.html',
		room = room,
		users = users,
	)
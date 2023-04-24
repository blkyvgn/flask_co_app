import sqlite3
from sqlalchemy.ext.horizontal_shard import ShardedSession
from flask_sqlalchemy.session import Session
from flask_sqlalchemy.model import Model
import sqlalchemy as sa
import sqlalchemy.orm


class AppModel(Model):
	pass
	''' Add Id to all tables by default '''
	# @sa.orm.declared_attr
	# def id(cls):
	# 	return sa.Column(sa.Integer, primary_key=True)

class AppSession(Session): # ShardedSession
	pass
import click
from flask.cli import AppGroup
from termcolor import colored
from app.extensions import db
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from app.vendors.helpers.config import cfg
from progress.bar import Bar
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)
from app.models import ( 
	Account, 
	Article,
	Category,
	Tag,
	Comment,
	Company,
)


user_cli = AppGroup('user')
@user_cli.command('create') 
@click.argument('email') 
@click.argument('password')
def create_user(email, password):
	if not email_validation_check(email):
		print(colored('Not valid email parametr', 'red')) 
		return

	if not passwd_validation_check(password):
		print(colored('Not valid password parametr', 'red')) 
		return

	user = db.session.execute(db.select(Account).filter_by(email=email)).scalar()
	if user is not None:
		print(colored('Account with such email already exist', 'red')) 
		return

	try:
		username = email.split('@')[0]
		new_user = Account(username=username, email=email, password=generate_password_hash(password)) 
		db.session.add(new_user)
		db.session.commit()
		print(colored(f'Account added: {email}', 'green'))
	except exc.SQLAlchemyError as e: 
		print(colored(f'Error while creating user: {email}\n {e})', 'red'))


@user_cli.command('list') 
def show_users():
	try:
		users = db.session.execute(db.select(Account)).scalars().all()
		print(users)
	except exc.SQLAlchemyError as e: 
		print(colored(f'Error while show users:\n {e})', 'red'))
from flask import (request, current_app,)
from email.mime.text import MIMEText
from app.vendors.helpers.config import cfg
from pathlib import Path
from .token import get_user_uid_token

from jinja2 import (
	Environment, 
	PackageLoader, 
	select_autoescape, 
	FileSystemLoader, 
)


def get_mail_body(html_template, **kwargs):
	template_path = Path(current_app.root_path) / current_app.template_folder
	env = Environment(
		loader=FileSystemLoader(template_path, encoding='utf-8'),
		autoescape=select_autoescape(['html', 'xml'])
	)
	template = env.get_template(html_template)
	return template.render(**kwargs)


def get_register_mail(user, html_template=None):
	subject = 'register subject'
	alias = ''
	if request.view_args:
		alias = request.view_args.get('alias', None)
	user_uid_token = '/'.join(get_user_uid_token(user).values())
	registration_link = f'{request.root_url}{alias}/auth/account_activate/{user_uid_token}'
	mail_data = {
		'sender': cfg('MAIL_DEFAULT_SENDER'),
		'to': user.email,
		'subject': subject,
		'registration_link': registration_link,
	}
	mail_data['html'] = get_mail_body(
		html_template, 
		subject = subject,
		sender = mail_data['sender'],
		registration_link = registration_link,
	)
	return mail_data
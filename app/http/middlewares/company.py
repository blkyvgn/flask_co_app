from app.extensions import babel 
from flask import session, request, g, abort
from app.vendors.helpers.config import cfg
from sqlalchemy.orm import exc
from app.extensions import db, cache
from app.models import Company


def company_middleware(app): 

	# @cache.cached(timeout=50, key_prefix='company')
	# def get_company(alias):
	# 	company = db.session.execute(
	# 		db.select(Company).filter_by(alias=alias)
	# 	).scalar()
	# 	return company

	@app.before_request 
	def gcompany():
		exclusion_list = ['static_root', 'static', 'api', 'socket.io']
		if request.endpoint not in exclusion_list:
			if request.view_args:
				alias = request.view_args.get('alias', cfg('COMPANY_ALIAS'))
				# company = get_company(alias)
				company = Company.get_from_cache(alias)
				if company is None:
					abort(404, 'Company not found', {'error_code': 1234})
				g.company = company

	@app.context_processor 
	def inject_lang():
		try:
			return {'company': g.company}
		except AttributeError:
			return {'company': None}
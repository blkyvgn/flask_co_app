

def registration_filters(app, jinja_filters): 
	""" configuration template filters """
	for _filter in jinja_filters:
		app.jinja_env.filters[_filter.name] = _filter.filter
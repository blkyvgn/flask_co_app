from flask import (session, g,)


__all__ = ('injects_context', )



def injects_context(app):
	# Add Curent User In Jinja2 Context (In Templates)
	@app.context_processor
	def inject_old():
		try:
			return { 
				'old': g.old, 
				'old_errors': g.old_errors
			}
		except AttributeError:
			return { 
				'old': None, 
				'old_errors': None,
			}

	@app.context_processor
	def inject_search():
		try:
			return { 
				# 'search_name': g.search,
				'search_name': session['search_name'],
			}
		except (KeyError, AttributeError):
			return { 
				'search_name': None, 
			}

def setup_context(app, context): 
	""" Configuration of middlewares """
	for handler in context:
		handler(app)
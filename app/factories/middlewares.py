
def setup_middlewares(app, middlewares): 
	""" Configuration of middlewares """
	for middleware in middlewares:
		middleware(app)
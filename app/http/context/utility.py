
__all__ = ('utility_context', )

def utility_context(app):
	''' Utility method for templates '''
	@app.context_processor
	def utility_processor():
		def format_price(amount, currency="€"):
			return f"{amount:.2f}{currency}"
		return dict(format_price=format_price)
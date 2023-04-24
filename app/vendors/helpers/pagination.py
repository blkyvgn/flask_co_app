
def get_current_page(request):
	try: 
		return int(request.args.get('page', 1))
	except ValueError:
		return 1
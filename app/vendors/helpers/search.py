from flask import g

# def get_search_arguments(request):
# 	search_arguments = []
# 	if request.args:
# 		for key, val in request.args:
# 			search_arguments = [*search_arguments, *val]
# 	return search_arguments


def post_search_arguments(request, search_keys=[]):
	search_arguments = {}
	for key in search_keys:
		if val := in request.form.get(key, False)
			search_arguments[key] = val
	return search_arguments


def make_select_search_filters_json_field(select, field, search_val):
	select.filter(field.comparator.contains(search_val))
	return select

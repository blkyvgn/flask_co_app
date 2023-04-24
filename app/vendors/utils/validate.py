from flask import request, g
from collections import namedtuple
from flask_babel import lazy_gettext as _l 
from flask_babel import _
from app.vendors.helpers import validators

__all__ = ('validate',)

Validator = namedtuple('Validator' , 'check message')

validators = {
	'required':     Validator(validators.required_check,      'Required field %s' ),
	'max':          Validator(validators.max_len_check,       'Too big %s'        ),
	'min':          Validator(validators.min_len_check,       'Too small %s'      ),
	'array_min':    Validator(validators.array_min_len_check, 'Too small array %s'),
	'unique':       Validator(validators.unique_check,        'Not unique %s'     ),
}


def validity_check(value, validator_keychain, exclude=None):
	validator_keys = validator_keychain.split('|')
	validation_errors = []
	for handler_key in validator_keys:
		name, *params = handler_key.split(':')
		if exclude and exclude in name:
			continue
		if validator := validators.get(name, False):
			if validator.check(value, *params) == False:
				msg = _l(validator.message % ','.join(params))
				validation_errors.append(msg)
		else:
			raise KeyError(f'Validator with name {name} not exist')

	return validation_errors

def get_value_by_key(key, postf):
	if 'array' in postf and 'file' in postf:
		value = request.files.getlist(key, None)
	elif 'file' in postf:
		value = request.files.get(key, None)
	elif 'array' in postf:
		value = request.form.getlist(key, None)
	else:
		value = request.form.get(key, None)
	return value


def validate():
	def _validate():
		pass 

	def post(key_validators={}, validators=validators):
		'''
		{
			'name': 'required|min:4|max:16',
			'short_desc': 'required|min:10|max:200',
			'count': 'required|int|int_min:50',
			'images:array:file': 'array_min:2|required|file_exts:jpg:png',
		}
		'''
		form_values = {key:val for key, val in request.form.items() if key != 'csrf_token'}
		form_validation_errors = {}
		is_valid = True

		for key, validator_keychain in key_validators.items():
			key, *postf = key.split(':')
			value = get_value_by_key(key, postf)
			if value:
				validation_errors = validity_check(
					value=value, validator_keychain=validator_keychain
				)
				if validation_errors:
					is_valid = False
				form_values[key] = value
				form_validation_errors[key] = validation_errors

				if 'array' in postf and isinstance(value, list):
					for index, val in enumerate(value):
						ind = index + 1
						validation_errors = validity_check(
							value=val, validator_keychain=validator_keychain, exclude='array'
						)
						if validation_errors:
							is_valid = False
						form_values[f'{key}:{ind}'] = val
						form_validation_errors[f'{key}:{ind}'] = validation_errors

			else:
				raise KeyError(f'Data with name {key} in request post not exist')
		
		if not is_valid:
			g.old = form_values
			g.old_errors = form_validation_errors
		return is_valid


	# def get(key_validators={}, validators=validators):
	# 	if request.args.get(key, False):
	# 		pass

	# def json(key_validators={}, validators=validators):
	# 	if request.json.get(key, False):
	# 		pass


	_validate.post = post
	# _validate.get = get
	# _validate.json = json
	return _validate



# ------------- simple ---------------
# def post(key_validators={}, validators=validators):
# 	form_old_values = {}
# 	form_validation_errors = {}
# 	is_valid = True

# 	# request.files[key]

# 	for key, validator_keychain in key_validators.items():
# 		if value := request.form.get(key, None):
# 			validator_keys = validator_keychain.split('|')
# 			validation_errors = []
# 			for handler_key in validator_keys:
# 				name, *params = handler_key.split(':')
# 				if validator := validators.get(name, False):
# 					if validator.check(value, *params) == False:
# 						msg = _l(validator.message % ','.join(params))
# 						validation_errors.append(msg)
# 						is_valid = False
# 				else:
# 					raise KeyError(f'Validator with name {name} not exist')
# 			form_old_values[key] = value
# 			form_validation_errors[key] = validation_errors
# 		else:
# 			raise KeyError(f'Data with name {key} in request post not exist')
	
# 	if not is_valid:
# 		g.old = form_old_values
# 		g.form_errors = form_validation_errors
# 	return is_valid
from six import text_type
from datetime import datetime
from app.vendors.helpers.config import cfg
import base64
import hashlib

# import hashlib
# a_string = '1'
# hashed_string = hashlib.sha256(a_string.encode('utf-8')).hexdigest()
# print(hashed_string)

def check_user_token(user, token):
	token_dict = eval(base64.b64decode(token))
	if token_raw := token_dict.get('token', False):
		token_parts = token_raw.split(':')
		return user.id == int(token_parts[0]) and token_parts[-2] == cfg('SECRET_KEY') and not eval(token_parts[-1])
	return False

def get_user_uid_token(user):
	uid = str({'uid': str(user.id)}).encode('utf-8')
	base64_uid = base64.b64encode(uid).decode('utf-8')
	token_raw = f'{str(user.id)}:{str(datetime.timestamp(datetime.now()))}:{cfg("SECRET_KEY")}:{str(user.is_activated)}'
	token = str({'token': token_raw}).encode('utf-8')
	base64_token = base64.b64encode(token).decode('utf-8')
	return {'uid': base64_uid, 'token':base64_token}

from app.extensions import api
from .account.resource import Account
print('--- 999999999999999999999999999 ---')
api.add_resource(Account, '/account/<int:pk>')

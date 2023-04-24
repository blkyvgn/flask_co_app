from .auth import auth_middleware
from .locale import locale_middleware
from .company import company_middleware

middlewares = [
	company_middleware,
	auth_middleware,
	locale_middleware,
]
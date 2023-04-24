from app.extensions import api
from .account.resource import AccountResource
from .auth.resource import (
	AccountRegisterResource,
	AccountLoginResource,
	AccountLogoutResource,
	TokenRefreshResource,
	AccountConfirmResource,
)
from .article.resource import (
	ArticleResource,
	ArticleListResource,
)
from .category.resource import (
	CategoryResource,
	CategoryListResource,
)

api.add_resource(AccountResource,             '/<string:alias>/api/account/<int:pk>/')
api.add_resource(ArticleResource,             '/<string:alias>/api/article/<int:pk>/')
api.add_resource(ArticleListResource,         '/<string:alias>/api/articles/')
api.add_resource(CategoryResource,            '/<string:alias>/api/category/<int:pk>/')
api.add_resource(CategoryListResource,        '/<string:alias>/api/categories/')
api.add_resource(AccountRegisterResource,     '/<string:alias>/api/register/')
api.add_resource(AccountLoginResource,        '/<string:alias>/api/login/')
api.add_resource(TokenRefreshResource,        '/<string:alias>/api/refresh/')
api.add_resource(AccountLogoutResource,       '/<string:alias>/api/logout/')
api.add_resource(AccountConfirmResource,      '/<string:alias>/api/account_confirm/<int:pk>/')

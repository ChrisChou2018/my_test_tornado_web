
# from app.handlers.api import api_account, api_member, api_welcome
from app.handlers.api import api_account
from app.handlers.api import api_items


urls = [
    (r"/v1/signin/?",                 api_account.ApiMemberSigninHandler),
    (r"/v1/register/?",               api_account.ApiMemberRegistrationHandler),
    (r"/v1/change_password_step1/?",  api_account.ApiChangePassStep1Handler),
    (r"/v1/change_password_step2/?",  api_account.ApiChangePassStep2Handler),
    (r"/v1/get_items/?",              api_items.ApiGetItemInfoHandler),
    (r"/v1/get_categories/?",         api_items.ApiGetCategoriesHandler),
    (r"/v1/filter_item/?",            api_items.ApiFilterItemHandler),
    (r"/v1/create_comment/?",         api_items.ApiCreateCommentHandler),
    (r"/v1/get_item_comment/?",       api_items.ApiGetItemCommentHandler),
]
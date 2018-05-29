
# from app.handlers.api import api_account, api_member, api_welcome
from app.handlers.api import api_account


urls = [
    # (r"/v1/member_info/?",          api_welcome.ApiMemberInfoHandler),
    # (r"/v1/register_member/?",      api_welcome.ApiRegisterMemberHandler),
    # (r"/v1/delete_member/?",        api_welcome.ApiDeleteMemberHandler),
    # (r"/v1/edit_member/?",          api_welcome.ApiEditMemberHandler),
    (r"/v1/signin/?",                 api_account.ApiMemberSigninHandler),
    (r"/v1/register/?",               api_account.ApiMemberRegistrationHandler),
    (r"/v1/change_password/?",        api_account.ApiChangePassHandler),
]
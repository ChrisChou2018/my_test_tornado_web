from app.handlers.admin import a_account
from app.handlers.admin import a_walcome


urls = [
    (r"/?",                                 a_walcome.AdminHomeHandler),
    (r"/member_manage/?",                   a_walcome.MemberManage),
    (r"/signin/?",                          a_account.AdminSigninHandler),
    (r"/signout/?",                         a_account.AdminSignoutHandler),
    (r"/register/?",                        a_account.AdminRegisterHandler),
    (r"/change_password/?",                 a_account.AdminChangePasswordHandler),
]

urls += [
    (r"/j/member_info/?",          a_walcome.AdminJsMemberInfoHandler),
    (r"/j/register_member/?",      a_walcome.AdminJsRegisterMemberHandler),
    (r"/j/delete_member/?",        a_walcome.AdminJsDeleteMemberHandler),
    (r"/j/edit_member/?",          a_walcome.AdminJsEditMemberHandler),
]
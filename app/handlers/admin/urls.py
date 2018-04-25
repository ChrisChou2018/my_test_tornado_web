from app.handlers.admin import a_account
from app.handlers.admin import a_walcome
from app.handlers.admin import api as admin_api


urls = [
    (r"/?",                                 a_walcome.AdminHomeHandler),
    (r"/j/add_job/?",                       a_walcome.AdminJsAddJobHandler),
    (r"/member_manage/?",                   a_walcome.MemberManage),
    (r"/signin/?",                          a_account.AdminSigninHandler),
    (r"/signout/?",                         a_account.AdminSignoutHandler),
    (r"/register/?",                        a_account.AdminRegisterHandler),
    (r"/change_password/?",                 a_account.AdminChangePasswordHandler),
    
]

urls += [
    (r"/v1/member_info/?",                  admin_api.ApiMemberInfoHandler),
]
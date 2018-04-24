from app.handlers.admin import a_account
from app.handlers.admin import a_walcome



urls = [
    (r"/?",                                 a_walcome.AdminHomeHandler),
    (r"/j/add_job/?",                       a_walcome.AdminJsAddJobHandler),
    (r"/signin/?",                          a_account.AdminSigninHandler),
    (r"/signout/?",                         a_account.AdminSignoutHandler),
    (r"/register/?",                        a_account.AdminRegisterHandler),
    (r"/change_password/?",                 a_account.AdminChangePasswordHandler),
]
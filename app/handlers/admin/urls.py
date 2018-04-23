from app.handlers.admin import a_account_view
from app.handlers.admin import a_walcome_view



urls = [
    (r"/?",                                 a_walcome_view.AdminHomeHandler),
    (r"/j/add_job/?",                       a_walcome_view.AdminJsAddJobHandler),
    (r"/signin/?",                          a_account_view.AdminSigninHandler),
    (r"/signout/?",                         a_account_view.AdminSignoutHandler),
    (r"/register/?",                        a_account_view.AdminRegisterHandler),
    (r"/change_password/?",                 a_account_view.AdminChangePasswordHandler),
]
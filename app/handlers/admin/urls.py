from app.handlers.admin.a_account_view import *
from app.handlers.admin.a_walcome_view import *



urls = [
    (r"/?",                                 AdminHomeHandler),
    (r"/signin/?",                          AdminSigninHandler),
    (r"/signout/?",                         AdminSignoutHandler),
    (r"/register/?",                        AdminRegisterHandler),
    (r"/j/add_job/?",                       AdminJsAddJobHandler),
]
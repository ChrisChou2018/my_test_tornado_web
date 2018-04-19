from app.handlers.admin.views import *


urls = [
    (r"/?",                               AdminHomeHandler),
    (r"/signin/?",                      AdminSigninHandler),
    (r"/signout/?",                     AdminSignoutHandler),
    (r"/register/?",                    AdminRegisterHandler),
    (r"/j/add_job/?",                   AdminJsAddJobHandler),
    # (r"/members/?",                     AdminMembersHandler),
    # (r"/members/vips/?",                AdminMemberVipsHandler),
    # (r"/member/detail/([a-z0-9-]+)/?", AdminMemberDetailHandler),
    # (r"/member/staff/([a-z0-9-]+)/?",   AdminMemberStaffHandler),
]
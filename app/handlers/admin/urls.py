from app.handlers.admin.views import *


urls = [
    (r"", AdminHomeHandler),
    (r"/j/add_job/?", AdminJsAddJobHandler),
    (r"/signin", AdminSigninHandler),
    (r"/signout", AdminSignoutHandler),
    (r"/members/?", AdminMembersHandler),
    (r"/members/vips/?", AdminMemberVipsHandler),
    # (r"/member/detail/([a-z0-9-]+)/?", AdminMemberDetailHandler),
    (r"/member/staff/([a-z0-9-]+)/?", AdminMemberStaffHandler),
]
from app.handlers.api import api_account, api_member, api_welcome


urls = [
    (r"/v1/member_info/?",          api_welcome.ApiMemberInfoHandler),
]
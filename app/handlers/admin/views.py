import tornado.web
import app.libs.data as data
# import app.models.goods_model as goods_model
# import app.models.order_model as order_model
import json
import datetime as dt
import time
from peewee import fn, SQL
# from app.models.goods_model import HomeLimitedGoods, Goods, Comment
from app.libs.handlers import SiteBaseHandler, ApiBaseHandler
from app.libs.decorators import admin_authenticated
import tornado.web
import app.models.member_model as member_model
# import app.models.coupon_model as coupon_model
from app.libs.handlers import JsSiteBaseHandler
from app.libs.decorators import has_permission
from app.models.member_model import Member
import string
import random
import hashlib
import uuid
# from datetime import *
import bcrypt
import re



'''
a_walcome
'''
# /admin
class AdminHomeHandler(SiteBaseHandler):
    @admin_authenticated
    def get(self):
        print(self.current_user)
        self.render("admin/a_index.html")


# /j/add_job
class AdminJsAddJobHandler(ApiBaseHandler):
    def get(self):
        # import app.models.rq_model as rq_model
        # import app.workers.wms_worker as wms_worker
        # order_data = {"order_id":"32132132131", "warehouse_id":"1231231231"}
        # rq_model.enqueue_job(wms_worker.wms_push_order, order_data)
        import os
        import uuid
        from PIL import Image
        # import app.models.goods_model as goods_model
        # import app.libs.picture as lib_picture
        source_path = os.path.join(self.settings["static_path"], "..", "localfile")

# /welcome/update_limited_goods_price/




'''
a_account.py
'''
# /admin/signin
class AdminSigninHandler(SiteBaseHandler):
    def get(self):
        self._render()

    def post(self):
        form_data = self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return

        # Update the storage of password.
        user_manager = Member.get_member_by_login(form_data["login_name"])
        if not user_manager:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return

        md5d = hashlib.md5(form_data["password"].encode(encoding='utf8')).hexdigest()
        user_hashpw = str(user_manager.hash_pwd)
        user_pwd = user_manager.password

        signin_flag = False
        if user_hashpw:
            if bcrypt.hashpw(md5d.encode('utf8'), user_hashpw.encode('utf8')) == user_hashpw.encode('utf8'):
                signin_flag = True
        elif user_pwd:
            if md5d == user_pwd:
                signin_flag = True
                hashd = bcrypt.hashpw(md5d.encode('utf8'), bcrypt.gensalt())
                user_manager.hash_pwd = hashd
                user_manager.password = ""

        if not signin_flag:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return

        sess_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
            for i in range(10)
        )
        session = {"id":sess_key, "time":int(time.time())}

        try:
            sessions = json.loads(user_manager.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)

        if len(sessions) > 5:
            sessions = sessions[-5:]

        user_manager.sessions = json.dumps(sessions)
        user_manager.save()

        self.set_cookie(self.settings["cookie_key_sess"],
            user_manager.member_id+":"+sess_key
        )

        self.redirect("/admin")

    def _list_form_keys(self):
        return ("login_name", "password")

    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_signin.html", form_data=form_data,
            form_errors=form_errors
        )

# /admin/signout
class AdminSignoutHandler(SiteBaseHandler):
    @tornado.web.addslash
    def get(self):
        self.clear_cookie(self.settings["cookie_key_sess"])
        self.redirect("/admin/signin")


class RegisterForm(object):
    def __init__(self):
        self.member_name = {'re':"^.{0,15}$", 'msg':'长度不超过15'}
        self.email = {'re':"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", 'msg':'邮箱格式不正确'}
        self.password = {'re':"^.{0,30}$", 'msg':'密码长度不超过30'}
        self.password2 = {'re':"^.{0,30}$", 'msg':'密码长度不超过30'}
    
    def check_valid(self, request):
        form_dict = self.__dict__
        flag = False
        clear_data = {}
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        if request.get_argument('password') != request.get_argument('password2'):
            return_data['status'] = False
            return_data['error_msg'] = {'password':'两次密码不一致'}
            return return_data
        elif not request.get_argument('password') or not request.get_argument('password2'):
            return_data['status'] = False
            return_data['error_msg'] = {'password':'密码不能为空'}
            return return_data
        for key, regular in form_dict.items():
            post_value = request.get_argument(key)
            # 让提交的数据 和 定义的正则表达式进行匹配
            ret = re.match(regular['re'], post_value)
            if not ret:
                break
            clear_data[key] = post_value
        else:
            flag = True
        
        


# /admin/register
class AdminRegisterHandler(SiteBaseHandler):
    def get(self):
        self._render()
    
    def post(self):
        form_data = self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return
        
    
    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_register.html", form_data=form_data,
            form_errors=form_errors
        )



# '''
# a_members
# '''
# class AdminMembersHandler(SiteBaseHandler):
#     @tornado.web.addslash
#     @has_permission("member")
#     def get(self):
#         member_id = self.get_argument("member_id", "")
#         telephone = self.get_argument("telephone", "")
#         is_staff = self.get_argument("is_staff", "")
#         if is_staff == "Y":
#             is_staff = True
#         elif is_staff == "N":
#             is_staff = False
#         else:
#             is_staff = None
#         vip_only = self.get_argument("vip_only", "")
#         is_vip = True if vip_only == "Y" else False
#         member_count = Member.list_members(
#             is_count=True, member_id=member_id, telephone=telephone, is_staff=is_staff,
#             is_vip=is_vip
#         )
#         members = [each for each in Member.list_members(
#             start=self.start, num=50, member_id=member_id, telephone=telephone,
#             is_staff=is_staff, is_vip=is_vip)
#         ]
#         self.render(
#             "a_members/a_members.html", member_id=member_id,
#             telephone=telephone, num=50, members=members,
#             is_staff=is_staff, member_count=member_count
#         )


# class AdminMemberVipsHandler(SiteBaseHandler):
#     """Member Vips
#     """
#     @tornado.web.addslash
#     @has_permission("member")
#     def get(self):
#         is_vip = True
#         member_count = Member.list_members(is_count=True, is_vip=is_vip)
#         members = [member_model.format_member(m) for m in Member.list_members(
#             start=self.start, num=50, is_vip=is_vip, orderby="last_vip_at_desc")]
#         self.render(
#             "a_members/a_member_vips.html", num=50, members=members, member_id="",
#             telephone="", member_count=member_count, is_staff=False
#         )


# class AdminMemberStaffHandler(JsSiteBaseHandler):
#     @tornado.web.addslash
#     @has_permission("member")
#     def post(self, member_id):
#         is_staff = self.get_argument("is_staff", "")
#         if is_staff == "N":
#             is_staff = False
#         else:
#             is_staff = True

#         member = Member.load_member_by_member_id(member_id)
#         if not member:
#             self.data["message"] = "没有该用户"
#             self.write(self.data)
#             return

#         Member.update_member({"telephone": member.telephone, "is_staff": is_staff})
#         self.data["result"] = "success"
        # self.write(self.data)

#!/usr/bin/env python
# coding:utf-8

import time
import json
import string
import random
import hashlib
import urllib
import uuid
import sys
from datetime import datetime, timedelta
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import os.path

import bcrypt
from PIL import Image, ImageDraw, ImageFont

from meihuishuo.libs.handlers import WwwBaseHandler, JsWwwBaseHandler
from meihuishuo.models.member_model import Member, MemberGrading, IdentifyingCode
from meihuishuo.libs.decorators import www_authenticated
import meihuishuo.libs.coupon as lib_coupon
from meihuishuo.models.shop_cart_model import ShopCart, app_update_cart
from meihuishuo.models.coupon_model import Coupon, Invitation
from meihuishuo.models.goods_model import Goods
from meihuishuo.libs.CCPRestSDK import REST
import meihuishuo.libs.social_sdk as social_sdk
from config_web import base_dir


class JsWwwMemberBase(WwwBaseHandler):
    # create and send code
    def _send_template_sms(self, to, datas, tempId):
        rest = REST(self.settings["sms_server_ip"],
                    self.settings["sms_server_port"],
                    self.settings["sms_soft_version"])
        rest.setAccount(self.settings["sms_account_sid"],
                        self.settings["sms_account_token"])
        rest.setAppId(self.settings["sms_app_id"])

        rest.sendTemplateSMS(to, datas, self.settings["sms_template_id"])

    def _create_send_identifying_code(self, telephone):
        flag = "success"
        tab = ""
        code = str(random.random())[3:9]
        time = datetime.now()
        IdentifyingCode.delete_code_by_telephone(telephone)
        IdentifyingCode.insert_code_by_telephone(telephone, code, time)

        if len(telephone) == 11:
            self._send_template_sms(telephone, [code, 2], "1")
            tab = "1"
        else:
            member = Member.find_telephone_by_memberid(telephone)
            if member:
                self._send_template_sms(telephone, [code, 2], "1")
                tab = "1"
            else:
                tab = "0"

        if tab == "0":
            IdentifyingCode.delete_code_by_telephone(telephone)
            flag = "error"
        return flag

    # send code help
    def send_code_help(self, telephone, action=None):
        member = Member.get_member_by_telephone(telephone)
        if member:
            if member.status == "1" and action == "registe":
                self.data["result"] = "error"
                self.data["status"] = "exists"
                self.data["message"] = "该电话号码已注册"
                return

            if action == "updatetel-new" or action == "bind_telephone":
                self.data["result"] = "error"
                self.data["message"] = "该电话号码已经注册"
                return
        else:
            if  action == "forgetpwd":
                self.data["result"] = "error"
                self.data["message"] = "该手机号没有在网站注册"
                return

        if (action == "updatetel-old" or action == "updatepwd") and \
                        self.current_user.telephone != telephone:
            self.data["result"] = "error"
            self.data["message"] = "该手机号不是您的注册手机号"
            return

        if len(telephone) == 11:
            is_num = True
            try:
                int(telephone)
            except Exception, e:
                is_num = False
            if is_num:
                ret = self._create_send_identifying_code(telephone)
        else:
            member1 = Member.find_telephone_by_memberid(telephone)
            if not member1:
                self.data["message"] = "用户不存在"
                return
            ret = self._create_send_identifying_code(member1.telephone)

        self.data["result"] = ret
        self.data["status"] = ret
        return

    # validate code
    def validate_code(self, code, member_id, action=None, overtime=2):
        flag = "error"
        identifying_code = IdentifyingCode.find_validate_code(code, member_id)
        if not identifying_code:
            return "codeError"

        now_time = datetime.now()
        end = time.mktime(now_time.timetuple())
        begin = time.mktime(identifying_code.create_time.timetuple())

        try:
            between_time = float(end-begin)/60
            if between_time > overtime:
                flag = "overtime"
            else:
                flag = "success"
        except Exception, e:
            flag = "error"
        if not action:
            IdentifyingCode.delete_code_by_telephone(member_id)

        return flag

    def login_help(self, telephone, password):
        if not telephone:
            self.data["message"] = u"用户名为空"
            return

        member = Member.get_member_by_login(telephone)
        if not member:
            self.data["message"] = u"用户不存在"
            return

        md5d = hashlib.md5(password).hexdigest()
        hash_pwd = str(member.hash_pwd)
        password = member.password

        signin_flag = False
        if hash_pwd and bcrypt.hashpw(md5d, hash_pwd) == hash_pwd:
            signin_flag = True

        if not signin_flag:
            self.data["message"] = u"密码错误"
            return

        try:
            member_grading = MemberGrading.get(MemberGrading.uuid == member.member_lvl)
            self.data["member_level"] = member_grading.name
        except Exception, e:
            self.data["member_level"] = u"普卡会员"
        cart_item_count = 0
        for each in ShopCart.get_app_cart_goods_list(member.member_id):
            cart_item_count += int(each.goods_count)
        self.data["member_name"] = member.member_name
        self.data["member_id"] = member.member_id
        self.data["message"] = u"登陆成功"
        self.data["result"] = "success"
        self.data["status"] = "success"
        self.data["cart_item_count"] = str(cart_item_count)
        sess_key = ''.join(random.choice(string.lowercase + string.digits)
                           for i in range(10))
        session = {"id": sess_key, "time": int(time.time())}

        try:
            sessions = json.loads(member.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)

        if len(sessions) > 5:
            sessions = sessions[-5:]

        member.sessions = json.dumps(sessions)
        member.save()
        self.data["session_id"] = sess_key
        self.data["message"] = ""

    def member_registration_help(self, password, telephone):
        Email = ""
        member = None
        if "@" in telephone:
            Email = telephone
            member = Member.get_member_by_email(telephone)
        else:
            member = Member.get_member_by_telephone(telephone)

        if member and member.status == "1":
            self.data["status"] = "error_telephone_exists"
            self.data["message"] = "电话号码已注册"
            return

        member_dict = dict()
        member_dict["telephone"] = telephone

        if member and member.status == "10":
            member_dict["member_id"] = member.member_id
        else:
            member_dict["member_id"] = str(uuid.uuid4()).replace("-", "")
            member_dict["member_id"] = member_dict["member_id"][0:15]

        member_dict["member_name"] = "MHS_" + str(random.random())[3:3+8]

        while True:
            member_name_exit = Member.get_member_by_member_name(member_dict["member_name"])
            if member_name_exit:
                member_dict["member_name"] = "MHS_" + str(random.random())[3:3 + 8]
            else:
                break

        # md5_password = hashlib.md5(password).hexdigest()
        md5d = hashlib.md5(password).hexdigest()
        member_dict["hash_pwd"] = bcrypt.hashpw(md5d, bcrypt.gensalt())
        MAX = sys.maxint
        MIN = int(MAX/2)
        member_dict["member_num"] = int(MIN+random.random()*(MAX-MIN))
        member_dict["create_time"] = datetime.now()
        member_dict["member_score"] = "0"
        member_dict["is_builtin"] = "0"
        member_dict["sessions"] = ""
        member_dict["status"] = "1"
        member_dict["email"] = Email
        if member and member.status == "10":
            Member.update_member(member_dict)
        else:
            Member.member_registration(member_dict)

        self.login_help(telephone, password)

        return

    # identify_message
    def identify_message(self, message):
        if message != "success":
            if message == "codeError":
                self.data["message"] = "短信验证码错误"
            elif message == "overtime":
                self.data["message"] = "验证超时"
            elif message == "error":
                self.data["message"] = "短信验证码不存在"
        return

    # pass help
    def change_password(self, code, telephone, new_password):
        self.data["result"] = "error"
        if not telephone or not code or not new_password:
            self.data["message"] = "请补全信息"
            return

        member = Member.get_member_by_login(Member.telephone == telephone)
        if not member:
            self.data["message"] = "用户不存在"
            return

        ret = self.validate_code(code, telephone)
        self.identify_message(ret)
        if ret != "success":
            return

        # member.password = hashlib.md5(password).hexdigest()
        md5d = hashlib.md5(new_password).hexdigest()
        hash_pwd = bcrypt.hashpw(md5d, bcrypt.gensalt())
        Member.update_pwd_by_telephone(telephone, hash_pwd)

        self.data["result"] = "success"
        self.data["message"] = ""
        return

    def login_handle(self, telephone, password):
        #
        # 注册成功后的自动登录的相关操作：
        #   1、新建 session
        #   2、设置 cookie
        #
        sess_key = ''.join(random.choice(string.lowercase + string.digits)
                           for i in range(10)
                           )
        session = {"id": sess_key, "time": int(time.time())}
        member = Member.get_member_by_login(telephone)
        try:
            sessions = json.loads(member.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)

        if len(sessions) > 5:
            sessions = sessions[-5:]

        member.sessions = json.dumps(sessions)
        member.save()

        self.set_cookie(self.settings["cookie_key_sess"],
                        member.member_id + ":" + sess_key)
        self.merge_shopcart(member)

    def login_by_code(self, telephone, code):
        """验证码登录．

        :param telephone:登录电话号码
        :param code: 验证码
        :return:
        """
        status = self.validate_code(code, telephone)
        if status != "success":
            self.identify_message(status)
            return

        member = Member.get_member_by_telephone(telephone)
        if not member:
            member = Member()
            now_time = datetime.now()
            member.member_id = str(uuid.uuid4()).replace("-", "")[0:15]
            member.telephone = telephone
            member.member_name = "MHS_" + str(random.random())[3:3+8]
            member.create_time = now_time
            member.update_time = now_time
            member.created_ip = self.client_ip
            member.status = "1"
            member.is_builtin = "0"
            member.member_lvl = MemberGrading.get_uuid_by_default()
            member.save(force_insert=True)

            lib_coupon.gen_coupon_by_condition(condition="register",
                                               member_id=member.member_id)

        self.login_session(member)

        self.data["status"] = "success"
        self.data["next_url"] = self.next_url
        return

    def login_session(self, member, merge_cart=True):
        sess_key = ''.join(random.choice(string.lowercase + string.digits)
                           for i in range(10)
                           )
        session = {"id": sess_key, "time": int(time.time())}

        try:
            sessions = json.loads(member.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)

        if len(sessions) > 5:
            sessions = sessions[-5:]

        member.sessions = json.dumps(sessions)
        member.save()

        # 合并登录前的购物车
        if merge_cart:
            self.merge_shopcart(member)

        self.clear_cookie(self.LOGIN_NEXT)

        self.set_cookie(self.settings["cookie_key_sess"],
                        member.member_id + ":" + sess_key)

    def merge_shopcart(self, member):
        #
        # 合并购物车
        #
        try:
            mhs_cart = urllib.unquote(self.get_cookie("mhs-cart"))
        except Exception as e:
            mhs_cart = None
        if mhs_cart:
            cart = json.loads(mhs_cart)
            items = cart['items']
            if items:
                goods_ids = []
                shopcart_goods_map = {}
                shocart_list = ShopCart.get_app_cart_goods_list(member.member_id)
                for cart in shocart_list:
                    goods_ids.append(cart.goods_id)
                    shopcart_goods_map[cart.goods_id] = cart

                cart_list = []  # 新添加的购物车
                update_list = []  # 需要更新的购物车信息
                create_time = datetime.now()+timedelta(seconds=1)
                for item in items:
                    if item['GoodsId'] not in goods_ids:
                        # 数据库没有该购物车商品
                        cart_dict = dict()
                        goods = Goods.get_goods_by_goods_id(item['GoodsId'])
                        if goods:
                            if goods.sale_type == "new_buyer":
                                cart_dict["goods_count"] = "1"
                            else:
                                cart_dict["goods_count"] = item['Count']
                            create_time = create_time - timedelta(seconds=1)
                            cart_dict["uuid"] = str(uuid.uuid4())
                            cart_dict["member_id"] = member.member_id
                            cart_dict["goods_id"] = item['GoodsId']
                            cart_dict["create_time"] = create_time
                            cart_list.append(cart_dict)

                if cart_list:
                    ShopCart.insert_many_items(cart_list)
                if update_list:
                    app_update_cart([], update_list, "new")


class WJsCheckcodeHandler(JsWwwMemberBase):
    def post(self):
        telephone = self.get_argument("telephone", None)
        action = self.get_argument("action", None)
        if not telephone:
            self.data["result"] = "error"
            self.data["message"] = "请输入手机号"
            self.write(self.data)
            return

        self.send_code_help(telephone, action)
        self.write(self.data)


class WSignoutHandler(WwwBaseHandler):
    def get(self):
        # self.clear_cookie(self.settings["cookie_key_sess"])
        self.clear_all_cookies()
        self.redirect("/")


class WLoginHandler(JsWwwMemberBase):
    def get(self):
        category_list = self.get_category()
        if self.current_user:
            self.redirect("/")
            return
        self._render(category_list=category_list)

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        code = self.get_argument("code", "")
        if not username and not username and not code:
            self.data["status"] = "error"
            self.data["message"] = "用户名/密码不能为空"
            self.write(self.data)
            return

        if code:
            self.login_by_code(username, code)
            self.write(self.data)
            return

        member = Member.get_member_by_login(username)
        if not member:
            self.data["status"] = "error"
            self.data["message"] = "用户名/密码不匹配"
            self.write(self.data)
            return

        login_flag = False
        md5d = hashlib.md5(password).hexdigest()
        user_pwd = str(member.hash_pwd)
        if user_pwd and bcrypt.hashpw(md5d, user_pwd) == user_pwd:
            login_flag = True

        if not login_flag:
            self.data["status"] = "error"
            self.data["message"] = "用户名/密码不匹配"
            self.write(self.data)
            return

        self.login_session(member)

        self.data["status"] = "success"
        self.data["next_url"] = self.next_url
        self.write(self.data)

    def _render(self, form_data=None, form_errors=None, category_list=[]):
        self.render("www/w_login.html",
                    form_data=form_data,
                    form_errors=form_errors)


class WJsUpdateTelOneHandler(JsWwwMemberBase):
    @www_authenticated
    def post(self):
        code = self.get_argument("code", None)
        telephone = self.get_argument("telephone", None)

        if telephone != self.current_user.telephone:
            self.data["message"] = "该手机号码不是当前使用手机号码"
            self.write(self.data)
            return

        ret = self.validate_code(code, self.current_user.telephone,
                                action="registe_stepone", overtime=10)

        self.identify_message(ret)
        if self.data["message"]:
            self.write(self.data)
            return

        self.data['status'] = "success"
        self.write(self.data)


class WJsUpdateTelTwoHandler(JsWwwMemberBase):
    @www_authenticated
    def post(self):
        code = self.get_argument("old_code", None)
        new_telephone = self.get_argument("new_telephone", None)
        new_code = self.get_argument("new_code", None)
        if not new_code or not new_telephone:
            self.data["result"] = "error"
            self.data["message"] = "请输入校验码或者新手机号"
            return

        telephone = self.current_user.telephone
        ret = self.validate_code(code, telephone)
        self.identify_message(ret)
        if ret != "success":
            self.write(self.data)
            return

        ret = self.validate_code(new_code, new_telephone)
        self.identify_message(ret)
        if ret != "success":
            self.write(self.data)
            return

        self.current_user.telephone = new_telephone
        self.current_user.save()

        self.data["status"] = "success"
        self.write(self.data)


class WJsUpdatePwdHandler(JsWwwMemberBase):
    @www_authenticated
    def post(self):
        code = self.get_argument("code", None)
        old_password = self.get_argument("old_password", None)
        new_password = self.get_argument("new_password", None)
        if not code or not old_password or not new_password:
            self.data["result"] = "error"
            self.data["message"] = "校验码或者密码为空"
            self.write(self.data)
            return

        md5d = hashlib.md5(old_password).hexdigest()
        hash_pwd = str(self.current_user.hash_pwd)
        md5_pwd = self.current_user.password

        validate_flag = False
        if hash_pwd and hash_pwd == bcrypt.hashpw(md5d, hash_pwd):
                validate_flag = True
        elif md5_pwd and md5_pwd == md5d:
                validate_flag = True

        if not validate_flag:
            self.data["result"] = "error"
            self.data["message"] = "旧密码错误"
            self.write(self.data)
            return

        telephone = self.current_user.telephone
        ret = self.validate_code(code, telephone, action="change_password")
        self.identify_message(ret)
        if ret != "success":
            self.data["result"] = "error"
            self.write(self.data)
            return

        self.change_password(code, telephone, new_password)
        # self.data["result"] = "success"
        self.write(self.data)


class WRegisteHandler(WwwBaseHandler):
    def get(self):
        category_list = self.get_category()
        if self.current_user:
            self.redirect("/")
        self.render("www/w_registe.html", category_list=category_list)


class WJsRegisteStepOneHandler(JsWwwMemberBase):
    def post(self):
        telephone = self.get_argument("telephone", None)
        if not telephone:
            self.data["status"] = "error"
            self.data["message"] = "请输入手机号"
            self.write(self.data)
            return

        validate = self.get_argument("validate", "")
        cookie_validate = self.get_secure_cookie("validate")
        if not validate or not cookie_validate:
            self.data["result"] = "error"
            self.data["message"] = "请输入正确的图片验证码"
            self.write(self.data)
            return

        if validate.lower() != cookie_validate.lower():
            self.data["result"] = "error"
            self.data["message"] = "图片验证码错误"
            self.write(self.data)
            return

        self.send_code_help(telephone, action="registe")  # "status": "exists"
        self.write(self.data)


class WJsRegisteStepTwoHandler(JsWwwMemberBase):
    def post(self):
        form_data = self._build_form_data()
        code = form_data["code"]
        telephone = form_data["telephone"]
        if not telephone:
            self.data["message"] = "电话号码为空"
            self.write(self.data)
            return

        password = form_data["password"]
        if len(password) < 6:
            self.data["message"] = "密码的长度要大于6"
            self.write(self.data)
            return

        # 图片验证码验证
        validate = form_data["validate"]
        cookie_validate = self.get_secure_cookie("validate")
        if validate.lower() != cookie_validate.lower():
            self.data["message"] = "图片验证码错误"
            self.write(self.data)
            return

        # 最后检查短信验证码
        da = self.validate_code(code, telephone)
        self.identify_message(da)
        if self.data["message"]:
            self.write(self.data)
            return

        member_status = Member.get_member_by_telephone(telephone)
        try:
            self.member_registration_help(password, telephone)
        except Exception, e:
            self.data["message"] = "请检查您的电话号码是否正确"
            self.write(self.data)
            return

        # 注册完后进行登录
        self.login_handle(telephone, password)

        coupons = coupon_sets = coupon_set_ids = coupon_list = invite_coupon_sets = []
        coupon_sum_value = 0

        if self.data["status"] == "success":
            coupon_sets = lib_coupon.gen_coupon_by_condition(condition="register",
                                                             member_id=self.data["member_id"])
            if member_status and member_status.status == "10":
                invite_coupon_sets = lib_coupon.gen_coupon_by_condition(
                    condition="invite", member_id=self.data["member_id"]
                )
                # Update the invitation record.
                # Then the inviter obtain the coupon.
                invitation_dict = {}
                invitation_dict["update_time"] = datetime.now()
                invitation_dict["status"] = "1"
                Invitation.update_invitation_by_invitee_id(self.data["member_id"],
                                                           invitation_dict)

                invitation_list = Invitation.list_invitation_by_invitee_id(self.data["member_id"])
                for invitation in invitation_list:
                    lib_coupon.gen_coupon_by_condition(condition="inviter",
                                                       member_id=invitation.inviter_id)

        if coupon_sets:
            coupon_set_ids = [each.coupon_set_id for each in coupon_sets]
        if invite_coupon_sets:
            for each in invite_coupon_sets:
                coupon_set_ids.append(each.coupon_set_id)

        if coupon_set_ids:
            coupon_list = Coupon.list_register_coupons(self.data["member_id"], coupon_set_ids)

        if coupon_list:
            for each in coupon_list:
                coupon_dict = dict()
                coupon_dict["coupon_id"] = each.coupon_id
                coupon_dict["avail_start_at"] = each.avail_start_at
                coupon_dict["avail_end_at"] = each.avail_end_at
                coupon_dict["coupon_set_name"] = each.coupon_set_name
                coupon_dict["face_value"] = str(each.face_value)
                coupon_dict["use_condition"] = str(each.use_condition)
                coupons.append(coupon_dict)
                coupon_sum_value = coupon_sum_value + each.face_value

        self.data["coupons"] = coupons
        self.data["coupon_sum_value"] = str(coupon_sum_value)
        self.write(self.data)

    def _list_form_keys(self):
        return ("password", "code", "telephone", "validate")


class WJsUpdateUserInfoHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        member_name = self.get_argument("member_name", None)
        year = self.get_argument("year", None)
        month = self.get_argument("month", None)
        day = self.get_argument("day", None)
        sex = self.get_argument("sex", None)
        if sex == "female":
            sex = u"女"
        else:
            sex = u"男"
        birthday = year + "-" + month + "-" + day

        if not member_name or not sex or birthday == "--":
            self.data["message"] = "个人信息不完整"
            self.write(self.data)
            return

        member_id = self.current_user.member_id
        member = Member.load_member_by_member_id(member_id)
        if not member:
            self.data["message"] = "用户已退出，请重新登录"
            self.write(self.data)
            return

        member.sex = sex
        member.birthday = birthday
        member.member_name = member_name
        member.save()

        self.data["result"] = "success"
        self.write(self.data)


class WForgetPwdHandler(WwwBaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/")

        self.render("www/w_forgetpwd.html")


class WJsForgetPwdHandler(JsWwwMemberBase):

    def post(self):
        code = self.get_argument("code", None)
        telephone = self.get_argument("telephone", None)
        password = self.get_argument("password", None)
        if not code or not password or not password:
            self.data["status"] = "error"
            self.data["message"] = "电话号码或校验码或者密码为空"
            self.write(self.data)
            return

        ret = self.validate_code(code, telephone, action="change_password")
        self.identify_message(ret)
        if ret != "success":
            self.data["status"] = "error"
            self.write(self.data)
            return

        self.change_password(code, telephone, password)

        sess_key = ''.join(random.choice(string.lowercase + string.digits)
                           for i in range(10)
                           )
        session = {"id": sess_key, "time": int(time.time())}

        member = Member.get_member_by_login(telephone)
        try:
            sessions = json.loads(member.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)

        if len(sessions) > 5:
            sessions = sessions[-5:]

        member.sessions = json.dumps(sessions)
        member.save()

        self.set_cookie(self.settings["cookie_key_sess"],
                        member.member_id + ":" + sess_key)

        self.data["status"] = "success"
        self.write(self.data)


class SociallAuthHandler(WwwBaseHandler):
    def get(self, provider):
        call_bacl_url = 'http://www.meihuishuo.com/callback/sociallogin?provider=' + provider
        url = ""
        if provider == "sina":
            client = social_sdk.WeiboAPIClient(app_key=self.settings["weibo_app_key"],
                                               app_secret=self.settings["weibo_app_secret"],
                                               redirect_uri=call_bacl_url)
            url = client.get_authorize_url()

        elif provider == "qq":
            client = social_sdk.QQAPIClient(app_key=self.settings["qq_app_id"],
                                            app_secret=self.settings["qq_app_key"],
                                            redirect_uri=call_bacl_url)
            url = client.get_authorize_url(status=client.status)

        elif provider == "weixin":
            client = social_sdk.WeixinAPIClient(app_key=self.settings["weixin_web_id"],
                                                app_secret=self.settings["weixin_web_key"],
                                                redirect_uri=call_bacl_url)
            url = client.get_authorize_url(status=client.status, scope=client.scope)

        if not url:
            self.redirect("/")
        else:
            self.redirect(url)


class WJsBindTelHandler(JsWwwMemberBase):
    """绑定手机号码"""
    def post(self):
        code = self.get_argument("code", None)
        telephone = self.get_argument("telephone", None)

        if not telephone or not code:
            self.data["message"] = "请填入需要绑定手机号和验证码"
            self.write(self.data)
            return

        validate_status = self.validate_code(code, telephone)
        if validate_status != "success":
            self.identify_message(validate_status)
            self.write(self.data)
            return

        if self.current_user.telephone:
            self.data["message"] = "您的手机号码已经绑定了哦～"
            self.write(self.data)
            return

        member = Member.get_member_by_telephone(telephone)
        if member:
            self.data["message"] = "您的手机号码已经注册了～ "
            self.write(self.data)
            return

        # 电话号码没有注册
        self.current_user.telephone = telephone
        self.current_user.save()
        self.data["status"] = "success"
        self.write(self.data)


class WJsSetPasswordHandler(JsWwwMemberBase):
    @www_authenticated
    def post(self):
        code = self.get_argument("code", "")
        password = self.get_argument("password", "")
        telephone = self.current_user.telephone

        if not telephone:
            self.data["message"] = "您没有绑定手机号码"
            self.write(self.data)
            return

        if not code:
            self.data["message"] = "验证码异常"
            self.write(self.data)
            return

        if len(password) > 16 or len(password) < 6:
            self.data["message"] = "密码的长度请控制在6~16位"
            self.write(self.data)
            return

        if self.current_user.hash_pwd:
            self.data["message"] = "您的账号已经设置了密码哦～"
            self.write(self.data)
            return

        validate_status = self.validate_code(code, telephone)
        if validate_status != "success":
            self.identify_message(validate_status)
            self.write(self.data)
            return

        self.current_user.hash_pwd = bcrypt.hashpw(hashlib.md5(password).hexdigest(),
                                                   bcrypt.gensalt())
        self.current_user.save()
        self.data["status"] = "success"
        self.write(self.data)

class WImageHandler(WwwBaseHandler):
    def get(self):
        # 字母:
        def rndChar():
            return chr(random.randint(65, 90))

        # 随机颜色1:
        def rndColor():
            return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

        # 随机颜色2:
        def rndColor2():
            return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

        width = 60 * 4
        height = 60
        image = Image.new('RGB', (width, height), (255, 255, 255))
        # 创建Font对象:
        font = ImageFont.truetype(os.path.join(base_dir, "assets/fonts/Mono-R.ttf"), 50)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)
        # 填充每个像素:
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=rndColor())

        # 输出并记录文字
        rand_str = ""
        for t in range(4):
            ch = rndChar()
            rand_str += ch
            draw.text((60 * t + 10, 10), ch, font=font, fill=rndColor2())

        stream = StringIO.StringIO()
        image.save(stream, "jpeg")
        stream_data = stream.getvalue()

        # 将 验证码写入 cookie
        self.set_secure_cookie("validate", rand_str)

        self.set_header('Content-Type','image/jpg')
        self.write(stream_data)

urls = [
    (r"/auth/([a-z0-9-]+)?", SociallAuthHandler),
    (r"/signin/?", WLoginHandler),
    (r"/signout/?", WSignoutHandler),
    (r"/registe/?", WRegisteHandler),
    (r"/registe/step1/?", WJsRegisteStepOneHandler),
    (r"/registe/step2/?", WJsRegisteStepTwoHandler),
    (r"/getcheckcode/?", WJsCheckcodeHandler),
    (r"/userinfo/update/?", WJsUpdateUserInfoHandler),
    (r"/userinfo/telephone/bind/?", WJsBindTelHandler),
    (r"/userinfo/telephone/update/stepone/?", WJsUpdateTelOneHandler),
    (r"/userinfo/telephone/update/steptwo/?", WJsUpdateTelTwoHandler),
    (r"/userinfo/password/update/?", WJsUpdatePwdHandler),
    (r"/userinfo/password/set/?", WJsSetPasswordHandler),
    (r"/password/forget/?", WForgetPwdHandler),
    (r"/password/reset/?", WJsForgetPwdHandler),

    (r"/image/?", WImageHandler),
]

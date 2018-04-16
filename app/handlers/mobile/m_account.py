# -*- coding: utf-8 -*-

import time
import json
import string
import random
import hashlib
from datetime import datetime
import uuid
import sys
import urllib
from datetime import datetime, timedelta

import bcrypt

from meihuishuo.libs.handlers import WwwBaseHandler, JsWwwBaseHandler
from meihuishuo.models.member_model import Member, IdentifyingCode, MemberGrading
from meihuishuo.models.shop_cart_model import ShopCart, app_update_cart
from meihuishuo.libs.decorators import www_authenticated
import meihuishuo.libs.coupon as lib_coupon
from meihuishuo.models.coupon_model import Coupon, Invitation
from meihuishuo.libs.CCPRestSDK import REST
from meihuishuo.models.goods_model import Goods


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

            if action == "updatetel-new":
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
                self.data["message"] = "验证码错误"
            elif message == "overtime":
                self.data["message"] = "验证超时"
            elif message == "error":
                self.data["message"] = "验证码不存在"
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
                            cart_dict["goods_count"] = item['Count']
                            cart_dict["create_time"] = create_time
                            cart_list.append(cart_dict)

                if cart_list:
                    ShopCart.insert_many_items(cart_list)
                if update_list:
                    app_update_cart([], update_list, "new")




class MJsCheckcodeHandler(JsWwwMemberBase):
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


class MSignoutHandler(JsWwwBaseHandler):
    def post(self):
        self.clear_all_cookies()

        self.data["result"] = "success"
        self.data["next"] = self.next_url
        self.write(self.data)

    def get(self):
        self.clear_all_cookies()

        self.redirect(self.next_url)


class MLoginHandler(JsWwwMemberBase):
    def get(self):
        if self.current_user:
            self.redirect("/")
            return

        self.render("m_mobile/m_login.html")

    def post(self):
        form_data = self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            self.data["status"] = "error"
            self.data["message"] = "用户名/密码不能为空"
            self.write(self.data)
            return

        member = Member.get_member_by_login(form_data["username"])
        if not member:
            self.data["status"] = "error"
            self.data["message"] = "用户名/密码不匹配"
            self.write(self.data)
            return

        login_flag = False
        md5d = hashlib.md5(form_data["password"]).hexdigest()
        user_pwd = str(member.hash_pwd)
        if user_pwd and bcrypt.hashpw(md5d, user_pwd) == user_pwd:
            login_flag = True

        if not login_flag:
            self.data["status"] = "error"
            self.data["message"] = "用户名/密码不匹配"
            self.write(self.data)
            return

        sess_key = ''.join(random.choice(string.lowercase + string.digits)
                           for _ in range(10)
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

        self.set_cookie(self.settings["cookie_key_sess"],
                        member.member_id + ":" + sess_key)

        self.clear_cookie(self.LOGIN_NEXT)

        self.merge_shopcart(member)

        self.data["status"] = "success"
        self.data["next_url"] = self.next_url
        self.write(self.data)

    def _list_form_keys(self):
        return ("username", "password")


class MRegisteHandler(JsWwwMemberBase):
    def get(self):
        if self.current_user:
            self.redirect("/signout")

        self.render("m_mobile/m_registe.html")

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
        self.data["next"] = self.next_url
        self.write(self.data)

    def _list_form_keys(self):
        return ("password", "code", "telephone")

class MMemberHandler(JsWwwBaseHandler):
    def get(self):
        current_user = self.current_user

        if not current_user:
            self.data["message"] = "您需要先登录"
            self.write(self.data)
        else:
            self.data["result"] = "success"
            self.data["message"] = {}
            self.data["message"]["login_name"] = current_user.login_name
            self.data["message"]["member_name"] = current_user.member_name
            self.data["message"]["member_lvl"] = current_user.member_lvl
            self.data["message"]["telephone"] = current_user.telephone
            self.write(self.data)


urls = [
    (r"/signin", MLoginHandler),
    (r"/signout", MSignoutHandler),
    (r"/member", MMemberHandler),
    (r"/registe", MRegisteHandler),
    (r"/getcheckcode/?", MJsCheckcodeHandler),
]

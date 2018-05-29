#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import random
from datetime import *
import time
import uuid
import sys
import string
import json

import bcrypt
import tornado.web


import app.models.member_model as member_model
from app.libs.handlers import ApiBaseHandler
from app.libs.decorators import api_authenticated



class ApiMemberBase(ApiBaseHandler):
    # create and send code
    # def create_send_identifying_code(self, telephone):
    #     flag = "success"
    #     tab = ""
    #     code = str(random.random())[3:9]
    #     time = datetime.now()
    #     IdentifyingCode.delete_code_by_telephone(telephone)
    #     IdentifyingCode.insert_code_by_telephone(telephone, code, time)

    #     if len(telephone) == 11:
    #         self.send_template_sms(telephone, [code, 5], "1")
    #         tab = "1"
    #     else:
    #         member = Member.find_telephone_by_memberid(telephone)
    #         if member:
    #             self.send_template_sms(telephone, [code, 5], "1")
    #             tab = "1"
    #         else:
    #             tab = "0"
    #     if tab == "0":
    #         IdentifyingCode.delete_code_by_telephone(telephone)
    #         flag = "error"
    #     return flag

    # # send code help
    # def send_code_help(self, telephone, api="register"):
    #     da = "error"
    #     if not telephone:
    #         self.data["result"] = da
    #         self.data["status"] = da
    #         self.data["message"] = "电话号码为空"
    #         return

    #     member = Member.get_member_by_telephone(telephone)
    #     if api in ("register", "new_telephone"):
    #         if member and member.status == "1":
    #             self.data["status"] = "error_telephone_exists"
    #             self.data["message"] = "电话号码已注册"
    #             return
    #     elif api in ("find_pass", "change_pass"):
    #         if not member:
    #             self.data["message"] = "用户不存在"
    #             return

    #     if len(telephone) == 11:
    #         is_num = True
    #         try:
    #             int(telephone)
    #         except Exception, e:
    #             is_num = False
    #         if is_num:
    #             da = self.create_send_identifying_code(telephone)
    #     else:
    #         member1 = Member.find_telephone_by_memberid(telephone)
    #         if not member1:
    #             self.data["message"] = "用户不存在"
    #             return
    #         da = self.create_send_identifying_code(member1.telephone)

    #     self.data["result"] = da
    #     self.data["status"] = da
    #     self.data["message"] = ""
    #     return

    # #validate code
    # def validate_code(self, code, member_id, api=False, overtime=5):
    #     flag = "error"
    #     identifying_code = IdentifyingCode.find_validate_code(code, member_id)
    #     if not identifying_code:
    #         return "codeError"

    #     now_time = datetime.now()
    #     end = time.mktime(now_time.timetuple())
    #     begin = time.mktime(identifying_code.create_time.timetuple())

    #     try:
    #         between_time = float(end-begin)/60
    #         if between_time > overtime:
    #             flag = "overtime"
    #         else:
    #             flag = "success"
    #     except Exception, e:
    #         flag = "error"

    #     if not api:
    #         IdentifyingCode.delete_code_by_telephone(member_id)

    #     return flag

    def login_help(self, telephone, password):
        if not telephone:
            self.data["message"] = "用户名为空"
            return

        member=  member_model.Member.get_member_by_login(telephone)
        if not member:
            self.data["message"] = "用户不存在"
            return

        salt_key = str(member.salt_key)
        member_hashpw = str(member.hash_pwd)
        signin_flag = False
        if member_hashpw:
            if bcrypt.hashpw((password+salt_key).encode(),
                    member_hashpw.encode()) == member_hashpw.encode():
                signin_flag = True

        if not signin_flag:
            self.data["message"] = u"密码错误"
            return

        self.data["status"] = "success"
        member.sessions, self.data["session_id"] = \
            self.set_login_session_and_write_data(member)
        member.sessions = json.dumps(member.sessions)
        member.save()

        # self._calc_vip_status(member)
        self.data["message"] = ""

    def member_registration_help(self, password, telephone):
        member = None
        member = member_model.Member.get_member_by_telephone(telephone)

        if member and member.status == "normal":
            self.data["status"] = "error_telephone_exists"
            self.data["message"] = "电话号码已注册"
            return

        member_dict = dict()
        member_dict["telephone"] = telephone

        member_dict["member_name"] = "MHS_" + str(random.random())[3:3+8]

        while True:
            member_name_exit =  member_model.Member.\
                get_member_by_member_name(member_dict["member_name"])
            if member_name_exit:
                member_dict["member_name"] = "MHS_" + str(random.random())[3:3+8]
            else:
                break

        random_salt_key = ''.join(
            random.choice(string.ascii_lowercase + string.digits) \
            for i in range(8)
        )
        haspwd = bcrypt.hashpw(
            (password+random_salt_key).encode(),
            bcrypt.gensalt()
        )
        member_dict["hash_pwd"] = haspwd
        member_dict["create_time"] = int(time.time())
        member_dict["update_time"] = int(time.time())
        member_dict["is_builtin"] = "0"
        member_dict["sessions"] = json.dumps(list())
        member_dict["status"] = "normal"
        member_dict["salt_key"] = random_salt_key
        # member_dict["email"] = Email
        member_model.Member.create_member(member_dict)
        self.login_help(telephone, password)
        return

    # # identify_message
    # def identify_message(self, message):
    #     if message != "success":
    #         if message == "codeError":
    #             self.data["message"] = "验证码错误"
    #         elif message == "overtime":
    #             self.data["message"] = "验证超时"
    #         elif message == "error":
    #             self.data["message"] = "验证码不存在"
    #     return

    # pass help
    def pass_help(self, api="find_pass"):
        telephone = self.get_argument("telephone", "")
        if api == "change_pass":
            telephone = self.current_user.telephone
        # code = self.get_argument("code", "")
        password = self.get_argument("password", "")

        if not telephone or not password:
            self.data["message"] = "请补全信息"
            return

        if len(password) > 16 or len(password) < 6:
            self.data["message"] = "密码的长度请控制在6~16位"
            return

        
        member =  member_model.Member.get_member_by_telephone(telephone)
        
        if not member:
            self.data["message"] = "用户不存在"
            return

        # da = self.validate_code(code, telephone)
        # self.identify_message(da)
        # if da != "success":
        #     return
        new_salt_key = ''.join(
            random.choice(string.ascii_lowercase + string.digits) \
            for i in range(8)
        )
        hashd = bcrypt.hashpw(
            (password + new_salt_key).encode('utf8'),
            bcrypt.gensalt()
        )
        member_model.Member.update_pwd(
            self.current_user.member_id,
            hashd
        )
        query = member_model.Member.update({'salt_key':new_salt_key}).\
            where(member_model.Member.member_id == self.current_user.member_id)
        query.execute()

        self.data["status"] = "success"
        self.data["message"] = ""
        return

    def set_login_session_and_write_data(self, member):
        sess_key = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for i in range(10)
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

        # self._calc_vip_status(member)
        # cart_item_count = 0
        # for each in ShopCart.list_cart_goods(member.member_id):
        #     cart_item_count += int(each.goods_count)
        self.data["member_name"] = member.member_name
        self.data["member_id"] = member.member_id
        self.data["status"] = "success"
        # self.data["cart_item_count"] = str(cart_item_count)
        # self.data["member_avatar"] = member.member_avatar

        return sessions, sess_key

    # def _calc_vip_status(self, member):
    #     if member.vip_avail_at < int(time.time()):
    #         self.data['member_level'] = u'普卡会员'
    #     else:
    #         self.data['member_level'] = u'VIP 星级用户'


class ApiMemberSigninHandler(ApiMemberBase):
    def post(self):
        
        login_name = self.get_argument("telephone", "")
        password = self.get_argument("password", "")

        # code = self.get_argument("code", "")
        # if code:
        if not login_name:
            self.data["message"] = "电话号码不正确"
            self.write(self.data)
            return

        if not login_name or not password:
            self.data["result"] = "error"
            self.data["message"] = "请补全账号密码"
            self.write(self.data)
            return

        self.login_help(login_name, password)
        self.write(self.data)

 

# class ApiRegisterCodeHandler(ApiMemberBase):
#     def post(self):
#         if not self.client_version:
#             self.send_error(403)
#             return

#         telephone = self.get_argument("MemberId", "")
#         if not telephone:
#             telephone = self.get_argument("telephone", "")

#         code_type = self.get_argument("code_type", "register")
#         # code_type:绑定电话号码:bind_telephone，设置密码:set_pass，验证码登录:auth
#         if not telephone and self.current_user:
#             telephone = self.current_user.telephone

#         self.send_code_help(telephone, code_type)
#         self.write(self.data)




class ApiMemberRegistrationHandler(ApiMemberBase):
    def post(self):
        form_data = self._build_form_data()
        # code = form_data["code"]
        telephone = form_data["telephone"]
        if not telephone:
            self.data["message"] = "电话号码为空"
            self.write(self.data)
            return

        # da = self.validate_code(code, telephone)
        # self.identify_message(da)
        # if self.data["message"]:
        #     self.write(self.data)
        #     return

        password = form_data["password"]
        if len(password) < 6:
            self.data["message"] = "密码的长度要大于6"
            self.write(self.data)
            return

        # member_status = member_model.Member.get_member_by_telephone(telephone)
        self.member_registration_help(password, telephone)
        if self.data['message']:
            self.write(self.data)
            return

        self.write(self.data)

    def _list_form_keys(self):
        return ("password", "telephone")


class ApiChangePassHandler(ApiMemberBase):
    @api_authenticated
    def post(self):
        self.pass_help(api="change_pass")
        self.write(self.data)


# class ApiSetPasswordHandler(ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         code = self.get_argument("code", "")
#         password = self.get_argument("password", "")
#         telephone = self.current_user.telephone

#         if not telephone or not code:
#             self.data["message"] = "参数有误"
#             self.write(self.data)
#             return

#         if len(password) > 16 or len(password) < 6:
#             self.data["message"] = "密码的长度请控制在6~16位"
#             self.write(self.data)
#             return

#         if self.current_user.hash_pwd:
#             self.data["message"] = "亲，您的账号已经有密码哦～"
#             self.write(self.data)
#             return

#         validate_status = self.validate_code(code, telephone)
#         if validate_status != "success":
#             self.identify_message(validate_status)
#             self.write(self.data)
#             return

#         self.current_user.hash_pwd = bcrypt.hashpw(
#             hashlib.md5(password).hexdigest(), bcrypt.gensalt()
#         )
#         self.current_user.save()
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiFindPassCodeHandler(ApiMemberBase):
#     def post(self):
#         telephone = self.get_argument("telephone", "")

#         self.send_code_help(telephone, api="find_pass")
#         self.write(self.data)


# class ApiFindPassHandler(ApiMemberBase):
#     def post(self):
#         self.pass_help()
#         self.write(self.data)


# class ApiChangePassCodeHandler(ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         password = self.get_argument("password", "")
#         if not password:
#             self.data["message"] = "密码为空"
#             self.write(self.data)
#             return

#         md5d = hashlib.md5(password).hexdigest()
#         hash_pwd = str(self.current_user.hash_pwd)
#         md5_pwd = self.current_user.password

#         validate_flag = False
#         if hash_pwd and hash_pwd == bcrypt.hashpw(md5d, hash_pwd):
#                 validate_flag = True
#         elif md5_pwd and md5_pwd == md5d:
#                 validate_flag = True

#         # if self.current_user.password != hashlib.md5(password).hexdigest():
#         if not validate_flag:
#             self.data["status"] = "error"
#             self.data["message"] = "密码错误"
#             self.write(self.data)
#             return
#         self.send_code_help(self.current_user.telephone, api="change_pass")
#         self.write(self.data)



# class ApiChangeTelephoneCodeHandler(ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         telephone = self.get_argument("telephone", "")
#         if not telephone:
#             telephone = self.current_user.telephone

#         # if self.current_user.telephone != telephone:
#         #     self.data["message"] = "电话号码和注册的电话号码不一致"
#         #     self.write(self.data)
#         #     return

#         self.send_code_help(telephone, api="change_telephone")
#         self.write(self.data)


# class ApiUpdatePwdHandler(ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         code = self.get_argument("Code", "")
#         member_id = self.get_argument("MemberId", "")
#         old_password = self.get_argument("OldPass", "")
#         new_password = self.get_argument("NewPass", "")
#         if not member_id:
#             code = self.get_argument("code", "")
#             member_id = self.get_argument("telephone", "")
#             old_password = self.get_argument("old_password", "")
#             new_password = self.get_argument("new_password", "")

#         validate_flag = self.validate_code(code, member_id)
#         if validate_flag != "success":
#             self.data["status"] = "error"
#             self.data["result"] = "error"
#             if validate_flag == "codeError":
#                 self.data["message"] = "验证码错误"
#             elif validate_flag == "overtime":
#                 self.data["message"] = "验证超时"
#             elif validate_flag == "error":
#                 self.data["message"] = "验证码不存在"
#             self.write(self.data)
#             return

#         new_md5d = hashlib.md5(new_password).hexdigest()
#         new_pass = bcrypt.hashpw(new_md5d, bcrypt.gensalt())
#         old_md5_pass = hashlib.md5(old_password).hexdigest()

#         member = Member.load_member_by_member_id(self.current_user.member_id)

#         validate_flag = False
#         if member:
#             if (member.hash_pwd and
#                     member.hash_pwd == bcrypt.hashpw(old_md5_pass, member.hash_pwd)):
#                 validate_flag = True
#             elif member.password and member.password == old_md5_pass:
#                 validate_flag = True

#         if not validate_flag:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "密码错误"
#             self.write(self.data)
#             return

#         Member.update_pwd(member.member_id, new_pass)

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiNewTelephoneCodeHandler(ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         code = self.get_argument("code", "")
#         telephone = self.get_argument("telephone", "")

#         da = self.validate_code(code, self.current_user.telephone,
#             api="step1", overtime=10
#         )

#         self.identify_message(da)
#         if self.data["message"]:
#             self.write(self.data)
#             return

#         if telephone:
#             if self.current_user.telephone == telephone:
#                 self.data["message"] = "亲，您的新手机号和旧手机号一样哦～"
#                 self.write(self.data)
#                 return

#             self.send_code_help(telephone, api="new_telephone")
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiChangeTelephoneHandler(ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         old_code = self.get_argument("old_code", "")
#         new_telephone = self.get_argument("new_telephone", "")
#         new_code = self.get_argument("new_code", "")

#         if new_telephone == self.current_user.telephone:
#             self.data["message"] = "亲，您的新手机号和旧手机号一样哦～"
#             self.write(self.data)
#             return

#         da1 = self.validate_code(old_code, self.current_user.telephone)
#         self.identify_message(da1)
#         if da1 != "success":
#             self.write(self.data)
#             return

#         da = self.validate_code(new_code, new_telephone)
#         self.identify_message(da)
#         if da != "success":
#             self.write(self.data)
#             return

#         self.current_user.telephone = new_telephone
#         self.current_user.save()

#         self.data["status"] = "success"
#         self.write(self.data)


# # /v1/refresh_status
# class ApiRefreshStatusHandler(ApiBaseHandler):
#     def get(self):
#         self.data["shopping_cart_item_count"] = 0
#         self.data["wait_pay_order_count"] = 0
#         self.data["wait_send_order_count"] = 0
#         self.data["wait_confirm_order_count"] = 0
#         self.data["wait_review_order_count"] = 0
#         self.data["avail_coupon_count"] = 0
#         self.data["inviter_coupon_sum"] = 0
#         self.data["avail_coupon_value"] = 0
#         self.data["gold_coin"] = 0
#         self.data["account_balance"] = 0
#         self.data["has_check_in"] = 'N'
#         self.data["has_new_version"] = "N"
#         self.data["new_version_intro"] = ""
#         self.data["status"] = "success"
#         self.data["version_name"] = ""
#         self.data["version_code"] = ""
#         self.data["apk_md5"] = ""
#         self.data["apk_url"] = ""
#         self.data["icon_avatar_url"] = ""
#         self.data["large_avatar_url"] = ""
#         self.data["promo_recall"] = "Y"
#         self.data["register_coupon_sum"] = 0
#         self.data["can_set_pwd"] = "N"
#         self.data["can_change_pwd"] = "N"
#         self.data["telephone"] = ""
#         self.data["skin_test_result"] = ""
#         self.data["skin_test_report_title"] = ""
#         self.data['vip_avail_at'] = 0
#         self.data['member_level'] = ''

#         if not self.current_user:
#             for each in CouponSet.list_coupon_set_by_dist_rule("register"):
#                 self.data["register_coupon_sum"] += each.face_value
#         else:
#             self.data['vip_avail_at'] = self.current_user.vip_avail_at
#             ts_now = int(time.time())
#             if self.current_user.vip_avail_at <= ts_now:
#                 self.data['member_level'] = '普卡会员'
#             else:
#                 self.data['member_level'] = 'VIP 星级用户'

#         version = Versions.load_version(self.platform)
#         if version:
#             if version.version_name != self.client_version:
#                 self.data["has_new_version"] = "Y"
#                 self.data["new_version_intro"] = version.update_content
#                 self.data["version_name"] = version.version_name
#                 self.data["version_code"] = version.version_code
#                 self.data["apk_md5"] = version.apk_md5
#                 self.data["apk_url"] = self.build_apk_url(version.file_name)

#         for each in CouponSet.list_coupon_set_by_dist_rule("inviter"):
#             self.data["inviter_coupon_sum"] += each.face_value

#         if not self.current_user:
#             self.data["signin_status"] = "none"
#             self.write(self.data)
#             return

#         self.data["gold_coin"] = self.current_user.gold_coin
#         self.data["account_balance"] = str(self.current_user.account_balance)

#         check_in_log = CheckinLog.load_nearest_checkin(self.current_user.member_id)
#         if check_in_log:
#             create_time = check_in_log.create_time.strftime("%Y-%m-%d")
#             now_time = datetime.now().strftime("%Y-%m-%d")
#             if create_time == now_time:
#                 self.data["has_check_in"] = 'Y'

#         if self.current_user.telephone:
#             self.data["telephone"] = self.current_user.telephone.replace(
#                 self.current_user.telephone[3:7], "****"
#             )
#             if not self.current_user.hash_pwd:
#                 self.data["can_set_pwd"] = "Y"
#             else:
#                 self.data["can_change_pwd"] = "Y"

#         for item in ShopCart.list_cart_goods(self.current_user.member_id):
#             self.data["shopping_cart_item_count"] += int(item.goods_count)
#         orders = Order.get_my_order(self.current_user.member_id, "0")
#         wait_review_order_ids = list()
#         for order in orders:
#             if order.status == "1":
#                 self.data["wait_pay_order_count"] += 1
#             elif order.status == "2":
#                 self.data["wait_send_order_count"] += 1
#             elif order.status == "3":
#                 self.data["wait_confirm_order_count"] += 1
#             elif order.status == "4":
#                 wait_review_order_ids.append(order.order_id)
#         order_goods = OrderGoods.list_order_goods_by_order_ids(
#             wait_review_order_ids
#         )
#         order_goods_ids = [each.goods_id for each in order_goods]
#         hava_comment_goods_ids = [each.goods_id for each in Comment.list_comment(
#             order_goods_ids, self.current_user.member_id)]
#         wait_review_order_list = list()
#         for goods in order_goods:
#             if goods.goods_id not in hava_comment_goods_ids:
#                 if goods.order_id not in wait_review_order_list:
#                     wait_review_order_list.append(goods.order_id)
#                     self.data["wait_review_order_count"] += 1

#         coupons = Coupon.list_coupons_by_status(
#             status="unused", owner_id=self.current_user.member_id,
#             now_time=int(time.time()), api_use="refresh_status"
#         )
#         for each in coupons:
#             self.data["avail_coupon_count"] += 1
#             self.data["avail_coupon_value"] += each.face_value
#         if self.current_user.member_avatar:
#             self.data["icon_avatar_url"] = self.build_photo_url(
#                 self.current_user.member_avatar, pic_version="thumb"
#             )
#             self.data["large_avatar_url"] = self.build_photo_url(
#                 self.current_user.member_avatar, pic_version="hd"
#             )

#         self.data["skin_test_result"] = self.current_user.skin_test_result \
#             if self.current_user.skin_test_result else "----"
#         if self.current_user.skin_test_result and '-' not in self.current_user.skin_test_result:
#             report = SkinTestReport.load_member_report(
#                 report_key=self.current_user.skin_test_result
#             )
#             self.data["skin_test_report_title"] = report.title if report else ""

#         self.data["signin_status"] = "normal"
#         self.write(self.data)


# class ApiSocialSigninHandler(ApiMemberBase):
#     def post(self):
#         form_data = self._build_form_data()
#         if not form_data["social_openid"] or \
#                 form_data["social_type"] not in ("qq", "sina", "wechat"):
#             self.data["status"] = "error"
#             self.data["message"] = "请选择第三方平台"
#             self.write(self.data)
#             return

#         member = Member.load_other_platform_member(
#             form_data["social_openid"], platform=form_data["social_type"]
#         )

#         if not member:
#             member = Member()
#             if form_data["social_type"] == "qq":
#                 member.qq_openid = form_data["social_openid"]
#             elif form_data["social_type"] == "wechat":
#                 member.wx_openid = form_data["social_openid"]
#             elif form_data["social_type"] == "sina":
#                 member.wb_openid = form_data["social_openid"]

#             now_time = datetime.now()
#             member.member_id = str(uuid.uuid4()).replace("-", "")
#             member.member_id = member.member_id[0:15]
#             member.create_time = now_time
#             member.update_time = now_time
#             member.member_name = form_data["screen_name"]
#             if form_data["gender"] == "0":
#                 member.sex = "女"
#             else:
#                 member.sex = "男"
#             member.access_token = form_data["access_token"]
#             member.member_avatar = form_data["profile_image_url"]
#             member.created_ip = self.client_ip
#             member.status = "1"
#             member.save(force_insert=True)

#             coupon_sets = list()
#             coupon_sum_value = 0
#             coupon_sets = lib_coupon.gen_coupon_by_condition(condition="register",
#                 member_id=member.member_id
#             )

#             if coupon_sets:
#                 for each in coupon_sets:
#                     coupon_sum_value = coupon_sum_value + each.face_value

#             self.data["coupon_sum_value"] = str(coupon_sum_value)

#         member.sessions, self.data["session_id"] = \
#             self.set_login_session_and_write_data(member)
#         member.sessions = json.dumps(member.sessions)
#         member.save()

#         self.write(self.data)

#     def _list_form_keys(self):
#         return ("social_openid", "social_type", "screen_name",
#             "gender", "access_token", "profile_image_url"
#         )





# class ApiInsertHandler(ApiBaseHandler):
#     # @api_authenticated
#     def post(self):
#         old_key = {"content": "Content", "opinions_type": "OpinionsType",
#                    "contact": "Contact"
#         }
#         new_key = {"content": "content", "opinions_type": "opinions_type",
#             "contact": "contact"
#         }
#         key = old_key
#         member_id = self.get_argument("MemberId", "")
#         if not member_id:
#             if self.current_user:
#                 member_id = self.current_user.member_id
#             else:
#                 member_id = ""
#             key = new_key

#         if not self.get_argument(key["content"], ""):
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "反馈的内容不能为空"
#             self.write(self.data)
#             return

#         opinion = Opinion()
#         opinion.title = "无标题"
#         opinion.opinion_id = str(uuid.uuid4())
#         opinion.create_time = datetime.now()
#         opinion.content = self.get_argument(key["content"], "")
#         opinion.opinions_type = self.get_argument(key["opinions_type"], "")
#         opinion.contact = self.get_argument(key["contact"], "")
#         opinion.create_person = member_id
#         opinion.status = "1"
#         opinion.save(force_insert=True)

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiUpdateInfoHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         member_name = self.get_argument("MemberName", "")
#         member_id = self.get_argument("MemberId", "")
#         sex = self.get_argument("Sex", "")
#         birthday = self.get_argument("Birthday", "")
#         if not member_id and not member_name:
#             member_name = self.get_argument("member_name", "")
#             member_id = self.current_user.member_id
#             sex = self.get_argument("sex", "")
#             birthday = self.get_argument("birthday", "")

#         if not birthday:
#             self.data["message"] = "请补充完整个人信息"
#             self.write(self.data)
#             return

#         try:
#             member = Member.load_member_by_member_id(member_id)
#         except Exception, e:
#             member = None

#         if not member:
#             self.data["message"] = "用户已退出，请重新登录"
#             self.write(self.data)
#             return

#         member.sex = sex if sex else member.sex
#         member.member_name = member_name if member_name else member.member_name
#         member.birthday = birthday
#         member.save()

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiInsertIOShandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         collect_person = self.get_argument("Addressee", "")
#         collect_address = self.get_argument("DetailAddress", "")
#         collect_tel = self.get_argument("Telephone", "")
#         member_id = self.get_argument("MemberId", "")
#         area = self.get_argument("Area", "")
#         if not member_id:
#             member_id = self.current_user.member_id
#             collect_person = self.get_argument("collect_person", "")
#             collect_tel = self.get_argument("collect_tel", "")
#             collect_address = self.get_argument("collect_address", "")
#             area = self.get_argument("area", "")

#         if not member_id or not collect_address or not collect_tel \
#                 or not collect_person or not area:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "请补全信息"
#             self.write(self.data)
#             return

#         address = Address()
#         address.addressee = collect_person
#         address.address = collect_address
#         address.telephone = collect_tel
#         address.member_id = member_id
#         address.area = area
#         address.address_id = str(uuid.uuid4())
#         address.create_time = datetime.now()
#         address.update_time = datetime.now()
#         address.save(force_insert=True)
#         if not self.current_user.default_address_id:
#             Member.update_member_by_member_ids([self.current_user.member_id],
#                 {"default_address_id": address.address_id}
#             )

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.data["address_id"] = address.address_id
#         self.write(self.data)


# class ApiFindListHandler(ApiBaseHandler):
#     @api_authenticated
#     def get(self):
#         old_key = {"address_id": "AddressId", "collect_address": "Address",
#             "collect_person": "Addressee", "collect_tel": "Telephone",
#             "area": "Area"
#         }
#         new_key = {"address_id": "address_id", "collect_address": "collect_address",
#             "collect_person": "collect_person", "collect_tel": "collect_tel",
#             "area": "area"
#         }
#         member_id = self.get_argument("MemberId", "")
#         key = old_key
#         if not member_id:
#             member_id = self.current_user.member_id
#             key = new_key

#         if not member_id:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "用户已退出，请重新登录"
#             self.write(self.data)
#             return

#         address = Address.find_all(member_id)

#         result = []
#         for each in address:
#             each_dict = dict()
#             each_dict[key["address_id"]] = each.address_id
#             each_dict[key["collect_address"]] = each.address
#             each_dict[key["collect_person"]] = each.addressee
#             each_dict[key["collect_tel"]] = each.telephone
#             each_dict[key["area"]] = each.area
#             each_dict["is_default"] = "N"
#             if self.current_user and \
#                     self.current_user.default_address_id == each.address_id:
#                 each_dict["is_default"] = "Y"
#                 result.insert(0, each_dict)
#                 continue

#             result.append(each_dict)

#         if key["address_id"] == "AddressId":
#             result_data = json.dumps(result)
#             self.set_header("Content-Type", "application/json; charset=UTF-8")
#             self.write(result_data)
#             return

#         self.data["status"] = "success"
#         self.data["addresses"] = result
#         self.write(self.data)


# class ApiDetailHandler(ApiBaseHandler):
#     @api_authenticated
#     def get(self):
#         old_key = {"address_id": "AddressId", "member_id": "MemberId",
#             "collect_person": "Addressee", "collect_address": "Address",
#             "collect_tel": "Telephone", "area": "Area", "zip_code": "ZipCode",
#             "create_time": "CreateTime", "update_time": "UpdateTime"
#         }
#         new_key = {"address_id": "address_id", "member_id": "member_id",
#             "collect_person": "collect_person", "collect_address": "collect_address",
#             "collect_tel": "collect_tel", "area": "area", "zip_code": "zip_code",
#             "create_time": "create_time", "update_time": "update_time"
#         }
#         key = old_key
#         address_id = self.get_argument("AddressId", "")
#         if not address_id:
#             address_id = self.get_argument("address_id", "")
#             key = new_key

#         if not address_id:
#             self.data["status"] = "error"
#             self.data["message"] = "获取数据出错"
#             self.write(self.data)
#             return

#         address = Address.find_by_id(address_id)
#         if address:
#             self.data["is_default"] = "N"
#             if self.current_user and self.current_user.default_address_id == address_id:
#                 self.data["is_default"] = "Y"

#             self.data[key["address_id"]] = address.address_id
#             self.data[key["member_id"]] = address.member_id
#             self.data[key["collect_person"]] = address.addressee
#             self.data[key["collect_address"]] = address.address
#             self.data[key["collect_tel"]] = address.telephone
#             self.data[key["area"]] = address.area
#             self.data[key["zip_code"]] = address.zip_code
#             self.data[key["create_time"]] = address.create_time.strftime(\
#                 '%Y-%m-%d %H:%M:%S')
#             self.data[key["update_time"]] = address.update_time.strftime(\
#                 '%Y-%m-%d %H:%M:%S')
#             self.data["status"] = "success"
#         self.write(self.data)


# class ApiUpdateIOShandler(ApiBaseHandler):
#     '''
#     线上API没有传MemberId和DetailAddress过来
#     现在需要改成判断MemberId是否为空，为空的话将返回错误信息
#     '''
#     @api_authenticated
#     def post(self):
#         address_id = self.get_argument("AddressId", "")
#         collect_person = self.get_argument("Addressee", "")
#         collect_address = self.get_argument("DetailAddress", "")
#         collect_tel = self.get_argument("Telephone", "")
#         member_id = self.get_argument("MemberId", "")
#         area = self.get_argument("Area", "")

#         if not member_id:
#             address_id = self.get_argument("address_id", "")
#             collect_person = self.get_argument("collect_person", "")
#             collect_address = self.get_argument("collect_address", "")
#             collect_tel = self.get_argument("collect_tel", "")
#             member_id = self.current_user.member_id
#             area = self.get_argument("area", "")

#         if not address_id and not collect_tel and not collect_address \
#                 and not collect_person and not area:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "请补全信息"
#             self.write(self.data)
#             return

#         try:
#             address = Address.get(Address.address_id == address_id)
#         except Exception, e:
#             address = None

#         if not address:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "请求出错"
#             self.write(self.data)
#             return

#         address.addressee = collect_person
#         address.address = collect_address
#         address.telephone = collect_tel
#         address.member_id = member_id
#         address.area = area
#         address.update_time = datetime.now()
#         address.save()

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiDeleteHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         address_id = self.get_argument("AddressId", "")
#         if not address_id:
#             address_id = self.get_argument("address_id", "")

#         if not address_id:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "网络错误"
#             self.write(self.data)
#             return

#         Address.delete_by_id(address_id)
#         if self.current_user.default_address_id == address_id:
#             default_address_id = ""
#             addresses = [each for each in \
#                 Address.list_address_by_member_id(self.current_user.member_id)]
#             if addresses:
#                 default_address_id = addresses[0].address_id

#             Member.update_member_by_member_ids([self.current_user.member_id],
#                 {"default_address_id": default_address_id}
#             )

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiMyCollectionListHandler(ApiBaseHandler):
#     @api_authenticated
#     def get(self):
#         member_id = self.current_user.member_id
#         goods = list()

#         goods_ids = [each.related_id for each in Collection.select().where(
#             Collection.member_id == member_id).order_by(Collection.create_time.desc())]
#         if not goods_ids:
#             self.data["status"] = "success"
#             self.data["goods"] = goods
#             self.write(self.data)
#             return

#         goods_list = goods_model.list_goods_min_price(goods_ids)

#         country_list = [each for each in Country.list_countries()]
#         current_type_list = [each for each in CurrencyType.list_currency_type()]

#         for g_id in goods_ids:
#             for each in goods_list:
#                 if each.goods_id == g_id:
#                     goods_dict = dict()
#                     goods_dict["type_intro"] = ""
#                     if each.sale_type == "new_buyer":
#                         goods_dict["type_intro"] = "新人专享"
#                     goods_dict["goods_id"] = each.goods_id
#                     goods_dict["goods_img_url"] = self.build_photo_url(each.img_view, pic_type="goods", cdn=True)
#                     goods_dict["buy_count"] = int(each.buy_count)
#                     goods_dict["goods_title"] = each.goods_title
#                     goods_dict["price"] = str(each.current_price)
#                     goods_dict["stock_count"] = int(each.stock)
#                     goods_dict["goods_brief_intro"] = each.abbreviation
#                     goods_dict["overseas_price"] = str(each.overseas_price)
#                     goods_dict["domestic_price"] = str(each.domestic_price)
#                     goods_dict["foreign_price"] = str(each.foreign_price)
#                     goods_dict["symbol"] = "￥"
#                     goods_dict["country_name"] = each.origin
#                     goods_dict["country_img_url"] = ""
#                     for c_t in current_type_list:
#                         if each.foreign_type == c_t.uuid:
#                             goods_dict["symbol"] = c_t.symbol
#                             break
#                     for country in country_list:
#                         if country.country_cn_name in each.origin:
#                             goods_dict["country_name"] = country.country_cn_name
#                             goods_dict["country_img_url"] = self.build_country_img_url(country.country_id)
#                             break
#                     goods.append(goods_dict)
#                     break

#         self.data["goods"] = goods
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiMemberInfoHandler(ApiBaseHandler):
#     '''
#     Api上没有这个接口
#     查看用户信息时要用到
#     '''
#     @api_authenticated
#     def get(self):
#         old_key = {"member_name": "MemberName", "sex": "Sex", "birthday": "Birthday"}
#         new_key = {"member_name": "member_name", "sex": "sex", "birthday": "birthday"}
#         key = old_key
#         member_id = self.get_argument("MemberId", "")
#         if not member_id:
#             member_id = self.current_user.member_id
#             key = new_key

#         try:
#             member_info = Member.load_member_by_member_id(member_id)
#         except Exception, e:
#             member_info = None

#         if not member_info:
#             self.data["status"] = "error"
#             self.data["message"] = "用户已退出，请重新登录"
#             self.write(self.data)
#             return

#         if member_info.member_name:
#             self.data[key["member_name"]] = member_info.member_name
#         if member_info.sex:
#             self.data[key["sex"]] = member_info.sex
#         if member_info.birthday:
#             self.data[key["birthday"]] = member_info.birthday

#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiUpdateAvatarHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         pic_dict = self._upload_photo()
#         if not pic_dict:
#             self.data["message"] = "头像上传失败"
#             self.write(self.data)
#             return

#         self.data["icon_avatar_url"] = self.build_photo_url(
#             pic_dict["picture_id"], "thumb"
#         )
#         self.data["large_avatar_url"] = self.build_photo_url(
#             pic_dict["picture_id"], "hd"
#         )
#         if self.current_user.member_avatar:
#             lib_picture.remove_picture(self.current_user.member_avatar,
#                 self.settings["static_path"], picture_type="avatar"
#             )

#         self.current_user.member_avatar = pic_dict["picture_id"]
#         self.current_user.save()
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiSetDefaultAddressHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         address_id = self.get_argument("address_id", "")
#         if not address_id:
#             self.data["message"] = "地址不存在"
#             self.write(self.data)
#             return

#         Member.update_member_by_member_ids([self.current_user.member_id],
#             {"default_address_id": address_id}
#         )
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiBindTelephoneHandler(ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         telephone = self.get_argument("telephone", "")
#         code = self.get_argument("code", "")

#         if not telephone or not code:
#             self.data["message"] = "参数有误"
#             self.write(self.data)
#             return

#         validate_status = self.validate_code(code, telephone)
#         if validate_status != "success":
#             self.identify_message(validate_status)
#             self.write(self.data)
#             return

#         if self.current_user.telephone:
#             self.data["message"] = "亲，您的电话号码已经绑定了哦～"
#             self.write(self.data)
#             return

#         member = Member.get_member_by_telephone(telephone)
#         if member:
#             self.data["message"] = "亲，您的号码已经注册了，赶紧登录去吧～ "
#             self.write(self.data)
#             return

#         # 电话号码没有注册
#         self.current_user.telephone = telephone
#         self.current_user.save()
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiCheckinHandler(ApiBaseHandler):
#     """签到处理"""
#     @api_authenticated
#     def post(self):
#         now = datetime.now()
#         current_user = self.current_user

#         check_in_count = 1
#         check_in_log = CheckinLog.load_nearest_checkin(current_user.member_id)
#         if check_in_log:
#             create_time = check_in_log.create_time.strftime("%Y-%m-%d")
#             now_time = now.strftime("%Y-%m-%d")
#             if create_time == now_time:
#                 # 今天已经签到
#                 self.data["message"] = "您今天已签到哦~"
#                 self.write(self.data)
#                 return
#             else:
#                 # 是否是连续签到, 相隔一天表示连续签到
#                 if (check_in_log.create_time +
#                         timedelta(days=1)).strftime("%Y-%m-%d") == now_time:
#                     check_in_count = check_in_log.checkin_count + 1

#         checkin_info = {}
#         checkin_info["member_id"] = current_user.member_id
#         checkin_info["create_time"] = now
#         checkin_info["update_time"] = now

#         # 确定连续签到时间
#         checkin_info["checkin_count"] = check_in_count
#         CheckinLog.insert_log(checkin_info)

#         today_coin_num, tomorrow_coin_num = self.get_checkin_coin(check_in_count)

#         coin_log = {}
#         coin_log["member_id"] = current_user.member_id
#         coin_log["create_time"] = now
#         coin_log["update_time"] = now
#         coin_log["coin_change"] = today_coin_num
#         coin_log["change_type"] = "checkin"
#         MemberCoinLog.insert_log(coin_log)

#         current_user.gold_coin += today_coin_num
#         current_user.save()

#         self.data["status"] = "success"
#         self.data["today_coin_num"] = today_coin_num
#         self.data["checkin_count"] = check_in_count
#         self.data["gold_coin"] = current_user.gold_coin
#         self.data["tomorrow_coin_num"] = tomorrow_coin_num
#         self.write(self.data)

#     def get_checkin_coin(self, check_in_count):
#         """根据签到连续的天数获取相应的金币"""
#         if check_in_count > 7:
#             return 20, 20
#         elif check_in_count == 7:
#             return 10, 20
#         else:
#             return 10, 10


# # /v1/account/redeem_vip_code
# class ApiRedeemVipCodeHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         vip_code = self.get_argument("vip_code", None)
#         if not vip_code:
#             self.data['message'] = ''
#             self.write(self.data)
#             return

#         coupon = Coupon.load_coupon_by_code(vip_code)
#         if not coupon:
#             self.data["message"] = "没有优惠券"
#             self.write(self.data)
#             return

#         coupon_set = CouponSet.load_coupon_set_by_id(
#             coupon.coupon_set_id
#         )
#         if not coupon_set:
#             self.data["message"] = "优惠券已过期"
#             self.write(self.data)
#             return
        
#         ts_now = int(time.time())
#         member = Member.load_member_by_member_id(self.current_user.member_id)
#         ts_start = ts_now if member.vip_avail_at == 0 or member.vip_avail_at <= ts_now \
#             else member.vip_avail_at

#         if coupon.face_value == 109:
#             member.vip_avail_at = ts_start + 183 * 24 * 3600
#         elif coupon.face_value == 199:
#             member.vip_avail_at = ts_start + 366 * 24 * 3600
#         member.save()
        
#         coupon.owner_id = self.current_user.member_id
#         coupon.dist_time = int(time.time())
#         coupon.save()

#         self.data["status"] = "success"
#         self.write(self.data)


# # /v1/account/balance_logs
# class ApiAccountBalanceLogsHandler(ApiBaseHandler):
#     @api_authenticated
#     def get(self):
#         self.data["balance_logs"] = member_model.list_account_balance_logs(self.current_user.member_id)
#         # self.data["balance_logs"] = list()
#         self.data["status"] = "success"
#         self.data["message"] = ""
#         self.write(self.data)


# urls = [
#     (r"/v1/login", ApiMemberSigninHandler),
#     (r"/v1/register_step1", ApiRegisterCodeHandler),
#     (r"/v1/register_step2", ApiMemberRegistrationHandler),
#     (r"/v1/register", ApiMemberRegistrationHandler),
#     (r"/v1/find_pass_step1", ApiFindPassCodeHandler),
#     (r"/v1/find_pass_step2", ApiFindPassHandler),
#     (r"/v1/change_pass_step1", ApiChangePassCodeHandler),
#     (r"/v1/change_pass_step2", ApiChangePassHandler),
#     (r"/v1/change_telephone_step1", ApiChangeTelephoneCodeHandler),
#     (r"/v1/change_telephone_step2", ApiNewTelephoneCodeHandler),
#     (r"/v1/change_telephone_step3", ApiChangeTelephoneHandler),
#     (r"/v1/refresh_status", ApiRefreshStatusHandler),
#     (r"/v1/social_signin", ApiSocialSigninHandler),
#     (r"/v1/account/update_password", ApiUpdatePwdHandler),
#     (r"/v1/feedbacks/create", ApiInsertHandler),
#     (r"/v1/account/update_profile", ApiUpdateInfoHandler),
#     (r"/v1/account/addresses/create", ApiInsertIOShandler),
#     (r"/v1/account/addresses", ApiFindListHandler),
#     (r"/v1/account/addresses/show", ApiDetailHandler),
#     (r"/v1/account/addresses/update", ApiUpdateIOShandler),
#     (r"/v1/account/addresses/destroy", ApiDeleteHandler),
#     (r"/v1/collections/", ApiMyCollectionListHandler),
#     (r"/v1/account_base_info", ApiMemberInfoHandler),
#     (r"/v1/update_avatar", ApiUpdateAvatarHandler),
#     (r"/v1/account/set_default_address", ApiSetDefaultAddressHandler),
#     (r"/v1/account/bind_telephone", ApiBindTelephoneHandler),
#     (r"/v1/account/set_pass", ApiSetPasswordHandler),
#     (r"/v1/account/checkin", ApiCheckinHandler),
#     (r'/v1/account/redeem_vip_code/?', ApiRedeemVipCodeHandler),
#     (r"/v1/account/balance_logs/?", ApiAccountBalanceLogsHandler),
# ]

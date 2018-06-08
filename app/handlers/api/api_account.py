#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import random
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
import config_web



class ApiMemberBase(ApiBaseHandler):
    def login_help(self, telephone, password):
        if not telephone:
            self.data["message"] = "用户名为空"
            return

        member=  member_model.Member.get_member_by_login(telephone)
        if not member:
            self.data["message"] = "用户不存在"
            return

        member_hashpw = member.hash_pwd
        signin_flag = False
        if member_hashpw:
            if bcrypt.checkpw(password.encode(),member_hashpw.encode()):
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

        member_dict["member_name"] = "UBS_" + str(random.random())[3:3+8]

        while True:
            member_name_exit =  member_model.Member.\
                get_member_by_member_name(member_dict["member_name"])
            if member_name_exit:
                member_dict["member_name"] = "UBS_" + str(random.random())[3:3+8]
            else:
                break

        haspwd = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )
        member_dict["hash_pwd"] = haspwd
        member_dict["create_time"] = int(time.time())
        member_dict["update_time"] = int(time.time())
        member_dict["is_builtin"] = "0"
        member_dict["sessions"] = json.dumps(list())
        member_dict["status"] = "normal"
        member_model.Member.create_member(member_dict)
        self.login_help(telephone, password)
        return

    def pass_help(self, api="find_pass"):
        telephone = self.get_argument("telephone", "")
        if api == "change_pass":
            telephone = self.current_user.telephone
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

        hashd = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )
        member_model.Member.update_pwd(
            self.current_user.member_id,
            hashd
        )

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
        self.data["member_name"] = member.member_name
        self.data["member_id"] = member.member_id
        self.data["status"] = "success"
        return sessions, sess_key


# /v1/signin/
class ApiMemberSigninHandler(ApiMemberBase):
    def post(self):
        login_name = self.get_argument("telephone", "")
        password = self.get_argument("password", "")
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


# /v1/register/
class ApiMemberRegistrationHandler(ApiMemberBase):
    def post(self):
        form_data = self._build_form_data()
        # code = form_data["code"]
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

        self.member_registration_help(password, telephone)
        if self.data['message']:
            self.write(self.data)
            return

        self.write(self.data)

    def _list_form_keys(self):
        return ("password", "telephone")


# /v1/change_password1/
class ApiChangePassStep1Handler(ApiMemberBase):
    @api_authenticated
    def post(self):
        password = self.get_argument("password", "")
        if not password:
            self.data["message"] = "密码为空"
            self.write(self.data)
            return

        member = self.current_user
        member_hashpw = member.hash_pwd
        validate_flag = False
        if member_hashpw:
            if bcrypt.checkpw(password.encode(),member_hashpw.encode()):
                validate_flag = True

        if not validate_flag:
            self.data["result"] = "error"
            self.data["message"] = "密码错误"
            self.write(self.data)
            return
        self.data['result'] = 'success'
        self.write(self.data)


# /v1/change_password2/
class ApiChangePassStep2Handler(ApiMemberBase):
    @api_authenticated
    def post(self):
        self.pass_help(api="change_pass")
        self.write(self.data)


import json
import time
import re
import os
import datetime as dt
import random
import string

import bcrypt

from app.libs import decorators
from app.libs import handlers
from app.models import member_model, items_model
import config_web


# /member_manage/
class AdminMemberManageHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        current_page = self.get_argument('page', 1)
        value = self.get_argument('search_value', None)
        filter_args = None
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = (
                (member_model.Member.member_name == value) | \
                (member_model.Member.telephone == value)
            )
            member_list = member_model.Member. \
                get_member_list(current_page, search_value)
            member_count = member_model.Member. \
                get_member_count(search_value)
        else:
            member_list = member_model.Member. \
            get_member_list(current_page)
            member_count = member_model.Member.get_member_count()
        uri = self.get_uri()
        self.render(
            "admin/a_member_manage.html", 
            member_list = member_list,
            member_count = member_count,
            current_page = current_page,
            filter_args = filter_args,
            uri = uri,
            search_value = value
        )


# /j/register_member/
class AdminJsRegisterMemberHandler(handlers.JsSiteBaseHandler):
    """
    注册用户接口
    """
    @decorators.js_authenticated
    def post(self):
        member = member_model.Member
        form_data = self._build_form_data()
        message = self._validate_form_data(form_data)
        if message is not None:
            self.data["message"] = message
            self.write(self.data)
            return

        member_obj_by_telephone = member. \
            get_member_by_telephone(form_data.get('telephone'))
        member_obj_by_name = member. \
            get_member_by_member_name(form_data.get('member_name'))
        if member_obj_by_telephone:
            self.data['message'] = '手机号码已经被注册'
        elif member_obj_by_name:
            self.data['message'] = '用户名已经存在'
        if self.data.get('message'):
            self.write(self.data)
            return

        pass_word = form_data['password']
        haspwd = bcrypt.hashpw(
            pass_word.encode(),
            bcrypt.gensalt()
        )
        form_data['hash_pwd'] = haspwd
        form_data.update({
            'sessions': json.dumps(list()),
            'status': 'normal',
            'role': 'admin',
            # 'salt_key': random_salt_key,
            'create_time': int(time.time()),
            'update_time': int(time.time())
        })
        member_model.Member.create_member(form_data)
        self.data['result'] = 'success'
        self.write(self.data)

    def _list_form_keys(self):
        return ("member_name", "telephone", "password", "password2")

    def _validate_form_data(self, form_data):
        message = None
        telephone = r"^1[3|4|5|8][0-9]\d{4,8}$"
        for key in self._list_form_keys():
            if not form_data[key]:
                message = "不能为空"
        if form_data['password'] != form_data['password2']:
            message = "两次密码不一致"
        if not re.match(telephone, form_data['telephone']):
            message = '手机号码不存在'
        if len(form_data['password']) > 30 or len(form_data['password']) < 6:
            message = '密码长度不超过30或不小于6位'
        if len(form_data['member_name']) > 15:
            message = '用户名长度不超过15'
        return message


# /j/delete_member/
class AdminJsDeleteMemberHandler(handlers.JsSiteBaseHandler):
    """
    删除用户接口
    """
    @decorators.js_authenticated
    def post(self):
        member_id_list = self.get_arguments('member_id_list[]')
        member = member_model.Member
        for i in member_id_list:
            member.update_member_by_member_id(i, {'status': 'deleted'})
        self.data['result'] = 'success'
        self.write(self.data)


# /j/edit_member/
class AdminJsEditMemberHandler(handlers.JsSiteBaseHandler):
    """
    编辑用户接口
    """
    @decorators.js_authenticated
    def get(self):
        member = member_model.Member
        member_id = self.get_argument('member_id', None)
        member_obj = member.get_member_by_id(member_id)
        self.data['data'] = {
            'member_id': member_id,
            'member_name': member_obj.member_name,
            'telephone': member_obj.telephone
        }
        self.data['result'] = 'success'
        self.write(self.data)

    @decorators.js_authenticated
    def post(self):
        member = member_model.Member
        member_id = self.get_argument('member_id', None)
        form_data = self._build_form_data()
        message = self._validate_form_data(form_data)
        if message is not None:
            self.data['result'] = message
            self.write(self.data)
            return
        clear_data = {key: form_data[key] for key in form_data if form_data[key]}
        if clear_data.get('telephone'):
            member_obj_by_telephone = member. \
                get_member_by_telephone(clear_data.get('telephone'))
            if member_obj_by_telephone:
                self.data['message'] = '手机号已经被注册'
        if clear_data.get('member_name'):
            member_obj_by_name = member. \
                get_member_by_name(clear_data.get('member_name'))
            if member_obj_by_name:
                self.data['message'] = '用户名已经存在'
        if self.data.get('message'):
            self.write(self.data)
            return
        if clear_data.get('password'):
            pass_word = clear_data.pop('password')
            clear_data.pop('password2')
            haspwd = bcrypt.hashpw(
                pass_word.encode(),
                bcrypt.gensalt()
            )
            clear_data['hash_pwd'] = haspwd
        member.update_member_by_member_id(member_id, clear_data)
        self.data['result'] = 'success'
        self.write(self.data)
        
    def _list_form_keys(self):
        return ("member_name", "telephone", "password", "password2")

    def _validate_form_data(self, form_data):
        message = None
        telephone = r"^1[3|4|5|8][0-9]\d{4,8}$"
        if  form_data['password'] and \
                form_data['password'] != form_data['password2']:
            message = "两次密码不一致"
        if form_data['telephone'] and \
                not re.match(telephone, form_data['telephone']):
            message = '手机号码不存在'
        if form_data['password'] and \
                len(form_data['password']) > 30 or \
                len(form_data['password']) < 6:
            message = '密码长度不超过30或不少于6位'
        if form_data['member_name'] and len(form_data['member_name']) > 15:
            message = '用户名长度不超过15'
        return message
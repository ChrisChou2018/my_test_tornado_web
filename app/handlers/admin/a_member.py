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
class MemberManage(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        current_page = self.get_argument('page', 1)
        value = self.get_argument('search_value', None)
        filter_args = None
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = ((member_model.Member.member_name == value) \
                            | (member_model.Member.email == value))
            member_obj = member_model.Member.get_member_obj(current_page, search_value)
            member_obj_count = member_model.Member.get_member_obj_count(search_value)
        else:
            member_obj = member_model.Member.get_member_obj(current_page)
            member_obj_count = member_model.Member.get_member_obj_count()
        if '?' in self.request.uri:
            url = self.request.uri.split('?')[0]
        else:
            url = self.request.uri
        self.render("admin/a_member_manage.html", member_obj = member_obj,
                                                  member_obj_count = member_obj_count,
                                                  current_page = current_page,
                                                  filter_args = filter_args,
                                                  url = url,
                                                  search_value = value)



# /j/register_member/
class AdminJsRegisterMemberHandler(handlers.JsSiteBaseHandler):
    """
    注册用户接口
    """
    @decorators.js_authenticated
    def post(self):
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        member = member_model.Member
        form_data = self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if not form_errors:
            return_data['status'] = False
            return_data["error_msg"] = form_errors
            self.write(json.dumps(return_data))
            return
        clear_data = return_data.get('clear_data')
        member_obj_by_email = member.get_member_by_email(clear_data.get('email'))
        member_obj_by_name = member.get_member_by_name(clear_data.get('member_name'))
        if member_obj_by_email:
            return_data['error_msg']['has_member_error'] = '邮箱已经被注册'
            return_data['status'] = False
        elif member_obj_by_name:
            return_data['error_msg']['has_member_error'] = '用户名已经存在'
            return_data['status'] = False
        if not return_data['status']:
            self.write(json.dumps(return_data))
            return
        pass_word = clear_data['password']
        random_salt_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
            for i in range(8)
        )
        haspwd = bcrypt.hashpw((pass_word+random_salt_key).encode(), bcrypt.gensalt())
        clear_data['hash_pwd'] = haspwd
        clear_data.update({'sessions':json.dumps(list()),
                           'status':'1',
                           'role':'admin',
                           'salt_key':random_salt_key,
                           'create_time':dt.datetime.now()})
        member.create(**clear_data)
        self.write(json.dumps({'status':True}))

    def _list_form_keys(self):
        return ("member_name", "email", "password", "password2")

    def _validate_form_data(self, form_data):
        form_errors = dict()
        email = r"^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$"
        for key in self._list_form_keys():
            if not form_data[key]:
                form_errors[key] = "不能为空"
        if form_data['password'] != form_data['password2']:
            form_errors['password'] = "两次密码不一致"
        if not re.match(email, form_data['email']):
            form_errors['email'] = '邮箱格式不正确'
        if len(form_data['password']) > 30:
            form_errors['password'] = '密码长度不超过30'
        if len(form_data['member_name']) > 15:
            form_errors['member_name'] = '用户名长度不超过15'
        return form_errors


# /j/delete_member/
class AdminJsDeleteMemberHandler(handlers.JsSiteBaseHandler):
    """
    删除用户接口
    """
    @decorators.js_authenticated
    def post(self):
        member_id_list = self.get_arguments('member_id_list[]')
        member = member_model.Member
        try:
            for i in member_id_list:
                obj = member.delete().where(member.member_id==i)
                obj.execute()
            self.write(json.dumps({'status':True}))
        except:
            self.write(json.dumps({'status':False,'error_msg':'出错'}))


# /j/edit_member/
class AdminJsEditMemberHandler(handlers.JsSiteBaseHandler):
    """
    编辑用户接口
    """
    @decorators.js_authenticated
    def get(self):
        return_data = {
            'data':None,
            'message':'',
            'status':True,
        }
        member = member_model.Member
        member_id = self.get_argument('member_id', None)
        try:
            member_obj = member.get(member.member_id==member_id)
            return_data['data'] = {'member_id':member_id,
                                'member_name':member_obj.member_name,
                                'email':member_obj.email}
            self.write(json.dumps(return_data))
        except Exception as error:
            return_data['status'] = False
            return_data['message'] = '服务器出错：{0}'.format(str(error))
            self.write(json.dumps(return_data))

    def post(self):
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        member = member_model.Member
        member_id = self.get_argument('member_id', None)
        form_data = self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            return_data['status'] = False
            return_data['error_msg'] = form_errors
            self.write(json.dumps(return_data))
            return
        clear_data = { key:form_data[key] for key in form_data if form_data[key] }
        if clear_data.get('email'):
            member_obj_by_email = member.get_member_by_email(clear_data.get('email'))
            if member_obj_by_email:
                return_data['error_msg']['has_member_error'] = '邮箱已经被注册'
                return_data['status'] = False
        if clear_data.get('member_name'):
            member_obj_by_name = member.get_member_by_name(clear_data.get('member_name'))
            if member_obj_by_name:
                return_data['error_msg']['has_member_error'] = '用户名已经存在'
                return_data['status'] = False
        if not return_data['status']:
            self.write(json.dumps(return_data))
            return
        if clear_data.get('password'):
            pass_word = clear_data.pop('password')
            clear_data.pop('password2')
            random_salt_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
                for i in range(8)
            )
            haspwd = bcrypt.hashpw((pass_word+random_salt_key).encode(), bcrypt.gensalt())
            clear_data['hash_pwd'] = haspwd
            clear_data.update({'salt_key':random_salt_key,})
        try:
            member.update_member_by_member_id(member_id, clear_data)
            self.write(json.dumps({'status':True}))
        except Exception as error:
            self.write(json.dumps({'status':False,
                                   'error_msg':{'server_error':'服务器错误{0}'.format(error)}}))

    def _list_form_keys(self):
        return ("member_name", "email", "password", "password2")

    def _validate_form_data(self, form_data):
        form_errors = dict()
        email = r"^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$"
        if  form_data['password'] and form_data['password'] != form_data['password2']:
            form_errors['password'] = "两次密码不一致"
        if form_data['email'] and not re.match(email, form_data['email']):
            form_errors['email'] = '邮箱格式不正确'
        if form_data['password'] and len(form_data['password']) > 30:
            form_errors['password'] = '密码长度不超过30'
        if form_data['member_name'] and len(form_data['member_name']) > 15:
            form_errors['member_name'] = '用户名长度不超过15'
        return form_errors
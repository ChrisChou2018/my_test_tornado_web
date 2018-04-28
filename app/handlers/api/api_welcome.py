#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.libs.decorators import admin_authenticated 
from app.libs.handlers import SiteBaseHandler
from app.models import member_model
from app import libs
import json
from app.handlers.form import form_account
from app.models import member_model
import bcrypt
import random
import string
import datetime as dt


class ApiMemberInfoHandler(SiteBaseHandler):
    """
    获取用户页面信息接口
    """
    @admin_authenticated
    def get(self):
        return_data = {
            'data':None,
            'message':'',
            'status':True,
            'page':'',
        }
        try:
            current_page = self.get_argument('page')
        except:
            current_page = 1
        member = member_model.Member
        table_head = ['member_id', 'member_name', 'email', 'role', 'more']
        member_obj = member.select().order_by(-member.member_id).paginate(int(current_page), 10)
        member_obj_count = member.select().count()
        page_obj = libs.Pagingfunc(current_page, member_obj_count)
        data_list = [[i.member_id, i.member_name, i.email, i.role] for i in member_obj]
        # self.set_header('Content-Type', 'application/json; charset=UTF-8')
        return_data['data'] = libs.create_html_table(table_head, data_list)
        return_data['page'] = page_obj.create_page_btn()
        self.write(json.dumps(return_data))


class ApiRegisterMemberHandler(SiteBaseHandler):
    """
    注册用户接口
    """
    @admin_authenticated
    def post(self):
        member = member_model.Member
        form_data = self._build_form_data()
        form_obj = form_account.RegisterForm()
        return_data = form_obj.check_valid(form_data)
        if not return_data['status']:
            self.write(json.dumps(return_data))
            return
        clear_data = return_data.get('clear_data')
        member_obj_by_email, member_obj_by_name = (member.get_member_by_email(clear_data.get('email')), 
                                                member.get_member_by_member_name(clear_data.get('member_name')))
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


class ApiDeleteMemberHandler(SiteBaseHandler):
    """
    删除用户接口
    """
    def post(self):
        try:
            member_id_list = self.get_arguments('member_id_list[]')
            member = member_model.Member
            for i in member_id_list:
                obj = member.delete().where(member.member_id==i)
                obj.execute()
            self.write(json.dumps({'status':True}))
        except:
            self.write(json.dumps({'status':False,'error_msg':'出错'}))


class ApiEditMemberHandler(SiteBaseHandler):
    """
    注册用户接口
    """
    def get(self):
        return_data = {
            'data':None,
            'message':'',
            'status':True,
        }
        member = member_model.Member
        try:
            member_id = self.get_argument('member_id', None)
            member_obj = member.get(member.member_id==member_id)
            return_data['data'] = {'f_member_id':member_id,
                                'f_member_name':member_obj.member_name,
                                'f_email':member_obj.email}
            self.write(json.dumps(return_data))
        except Exception as error:
            return_data['status'] = False
            return_data['message'] = '服务器出错：{0}'.format(str(error))
            self.write(json.dumps(return_data))

    def post(self):
        member = member_model.Member
        member_id = self.get_argument('member_id', None)
        form_data = self._build_form_data()
        form_obj = form_account.RegisterForm()
        return_data = form_obj.check_valid(form_data, is_edit=True)
        if not return_data['status']:
            self.write(json.dumps(return_data))
            return
        clear_data = return_data.get('clear_data')
        if clear_data.get('email'):
            member_obj_by_email = member.get_member_by_email(clear_data.get('email'))
            if member_obj_by_email:
                return_data['error_msg']['has_member_error'] = '邮箱已经被注册'
                return_data['status'] = False
        if clear_data.get('member_name'):
            member_obj_by_name = member.get_member_by_member_name(clear_data.get('member_name'))
            if member_obj_by_name:
                return_data['error_msg']['has_member_error'] = '用户名已经存在'
                return_data['status'] = False
        if not return_data['status']:
            self.write(json.dumps(return_data))
            return
        if clear_data.get('password'):
            pass_word = clear_data['password']
            random_salt_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
                for i in range(8)
            )
            haspwd = bcrypt.hashpw((pass_word+random_salt_key).encode(), bcrypt.gensalt())
            clear_data['hash_pwd'] = haspwd
            clear_data.update({'salt_key':random_salt_key,})
        try:
            query = member.update(clear_data).where(member.member_id == member_id)
            query.execute()
            self.write(json.dumps({'status':True}))
        except Exception as error:
            self.write(json.dumps({'status':False, 'error_msg':'服务器错误{0}'.format(error)}))
    def _list_form_keys(self):
        return ("member_name", "email", "password", "password2",)
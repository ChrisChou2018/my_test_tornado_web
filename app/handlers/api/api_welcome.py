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
        table_head = ['member_id', 'member_name', 'email', 'role']
        member_obj = member.select().order_by(-member.member_id).paginate(int(current_page), 10)
        member_obj_count = member.select().count()
        page_obj = libs.Pagingfunc(current_page, member_obj_count)
        data_list = [[i.member_id, i.member_name, i.email, i.role] for i in member_obj]
        # self.set_header('Content-Type', 'application/json; charset=UTF-8')
        return_data['data'] = libs.create_html_table(table_head, data_list)
        return_data['page'] = page_obj.create_page_btn()
        self.write(json.dumps(return_data))


class ApiRegisterMemberHandler(SiteBaseHandler):
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

        
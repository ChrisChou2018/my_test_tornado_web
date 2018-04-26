#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.libs.decorators import admin_authenticated 
from app.libs.handlers import SiteBaseHandler
from app.models.member_model import Member
from app.libs import Pagingfunc, create_html_table
import json




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
        table_head = ['member_id', 'member_name', 'email', 'role']
        member_obj = Member.select().paginate(int(current_page), 10)
        member_obj_count = Member.select().count()
        page_obj = Pagingfunc(current_page, member_obj_count)
        data_list = [[i.member_id, i.member_name, i.email, i.role] for i in member_obj]
        # self.set_header('Content-Type', 'application/json; charset=UTF-8')
        return_data['data'] = create_html_table(table_head, data_list)
        return_data['page'] = page_obj.create_page_btn()
        self.write(json.dumps(return_data))
        



        
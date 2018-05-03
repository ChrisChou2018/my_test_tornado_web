from app.libs import decorators
from app.libs import handlers
from app import libs
from app.models import member_model
import json
import config_web
import bcrypt
import random
import string
import datetime as dt
import re
# /
class AdminHomeHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        self.render("admin/a_index.html")



# /member_manage/
class MemberManage(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        try:
            current_page = self.get_argument('page')
        except:
            current_page = 1
        member = member_model.Member
        try:value = self.get_argument('search_value')
        except:value=None
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = ((member.member_name == value) | (member.email == value))
        else:
            filter_args = None
            search_value = None
        table_head = ['member_id', 'member_name', 'email', 'role', 'more']
        if not search_value:
            member_obj = member.select().order_by(-member.member_id).paginate(int(current_page), 15)
            member_obj_count = member.select().count()
        else:
            member_obj = member.select().where(search_value).order_by(-member.member_id).paginate(int(current_page), 15)
            member_obj_count = member.select().where(search_value).count()
        # page_obj = libs.Pagingfunc(current_page, member_obj_count, filter_args=filter_args)
        if '?' in self.request.uri:
            url, arg = self.request.uri.split('?')
        else:
            url = self.request.uri
        self.render("admin/a_member_manage.html",**{'member_obj':member_obj,
                                                    'table_head':table_head,
                                                    'member_obj_count':member_obj_count,
                                                    'current_page':current_page,
                                                    'filter_args':filter_args,
                                                    'url':url,
                                                    'search_value':value})



# class AdminJsMemberInfoHandler(handlers.JsSiteBaseHandler):
#     """
#     获取用户页面信息接口
#     """
#     @decorators.js_authenticated
#     def get(self):
#         return_data = {
#             'data':None,
#             'message':'',
#             'status':True,
#             'page':'',
#         }
#         try:
#             current_page = self.get_argument('page')
#         except:
#             current_page = 1
#         member = member_model.Member
#         try:
#             value = self.get_argument('search_value')
#             filter_args = 'search_value={0}'.format(value)
#             search_value = ((member.member_name == value) | (member.email == value))
#         except:
#             filter_args = None
#             search_value = None
#         table_head = ['member_id', 'member_name', 'email', 'role', 'more']
#         if not search_value:
#             member_obj = member.select().order_by(-member.member_id).paginate(int(current_page), 10)
#             member_obj_count = member.select().count()
#         else:
#             member_obj = member.select().where(search_value).order_by(-member.member_id).paginate(int(current_page), 10)
#             member_obj_count = member.select().where(search_value).count()
#         page_obj = libs.Pagingfunc(current_page, member_obj_count, filter_args=filter_args)
#         data_list = [[i.member_id, i.member_name, i.email, i.role] for i in member_obj]
#         # self.set_header('Content-Type', 'application/json; charset=UTF-8')
#         return_data['data'] = libs.create_html_table(table_head, data_list)
#         return_data['page'] = page_obj.create_page_btn()
#         self.write(json.dumps(return_data))



class RegisterForm(object):
    """
    注册和编辑用户form验证，默认是添加用户验证如果是编辑用户验证，
    将check_valid中的is_edit变为true即可
    """
    def __init__(self):
        self.member_name = {'re':r"^.{0,15}$", 'msg':'长度不超过15'}
        self.email = {'re':r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", 'msg':'邮箱格式不正确'}
        self.password = {'re':r"^.{0,30}$", 'msg':'密码长度不超过30'}
        self.password2 = {'re':r"^.{0,30}$", 'msg':'密码长 度不超过30'}
    
    def check_valid(self, form_data, is_edit = False):
        form_dict = self.__dict__
        clear_data = {}
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        if form_data.get('password') != form_data.get('password2'):
            return_data['error_msg'] = {'password':'两次密码不一致'}
        elif not form_data.get('password') or not form_data.get('password2'):
            if is_edit:
                pass
            else:
                return_data['error_msg'] = {'password':'密码不能为空'}
        elif not form_data.get('member_name'):
            if  is_edit:
                pass
            else:
                return_data['error_msg'] = {'member_name':'昵称不能为空'}
        elif not form_data.get('email'):
            if is_edit:
                pass
            else:
                return_data['error_msg'] = {'email':'邮箱不能为空'}
        if return_data['error_msg']:
            return_data['status'] = False
            return return_data
        for key, regular in form_dict.items():
            post_value = form_data.get(key)
            # 让提交的数据 和 定义的正则表达式进行匹配
            if post_value:
                ret = re.match(regular['re'], post_value)
                if not ret:
                    return_data['status'] = False
                    return_data['error_msg'] = {key:regular['msg']}
                    return return_data
                clear_data[key] = post_value
        else:
            return_data['clear_data'] = clear_data
            return return_data


class AdminJsRegisterMemberHandler(handlers.JsSiteBaseHandler):
    """
    注册用户接口
    """
    @decorators.js_authenticated
    def post(self):
        member = member_model.Member
        form_data = self._build_form_data()
        form_obj = RegisterForm()
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



class AdminJsDeleteMemberHandler(handlers.JsSiteBaseHandler):
    """
    删除用户接口
    """
    @decorators.js_authenticated
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



class AdminJsEditMemberHandler(handlers.JsSiteBaseHandler):
    """
    注册用户接口
    """
    @decorators.js_authenticated
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
            return_data['data'] = {'member_id':member_id,
                                'member_name':member_obj.member_name,
                                'email':member_obj.email}
            self.write(json.dumps(return_data))
        except Exception as error:
            return_data['status'] = False
            return_data['message'] = '服务器出错：{0}'.format(str(error))
            self.write(json.dumps(return_data))

    def post(self):
        member = member_model.Member
        member_id = self.get_argument('member_id', None)
        form_data = self._build_form_data()
        form_obj = RegisterForm()
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



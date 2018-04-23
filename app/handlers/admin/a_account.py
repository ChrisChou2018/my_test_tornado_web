
from app.libs.handlers import SiteBaseHandler
from app.models.member_model import Member
import hashlib
import bcrypt
import random
import string
import time
import datetime as dt
import json
import tornado.web
import re


# /signin/
class AdminSigninHandler(SiteBaseHandler):
    def get(self):
        self._render()

    def post(self):
        form_data = self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return

        # Update the storage of password.
        user_manager = Member.get_member_by_login(form_data["login_name"])
        if not user_manager:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return

        md5d = hashlib.md5(form_data["password"].encode(encoding='utf8')).hexdigest()
        user_hashpw = str(user_manager.hash_pwd)
        user_pwd = user_manager.password

        signin_flag = False
        if user_hashpw:
            if bcrypt.hashpw(md5d.encode('utf8'), user_hashpw.encode('utf8')) == user_hashpw.encode('utf8'):
                signin_flag = True
        elif user_pwd:
            if md5d == user_pwd:
                signin_flag = True
                hashd = bcrypt.hashpw(md5d.encode('utf8'), bcrypt.gensalt())
                user_manager.hash_pwd = hashd
                user_manager.password = ""

        if not signin_flag:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return

        sess_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
            for i in range(10)
        )
        session = {"id":sess_key, "time":int(time.time())}

        try:
            sessions = json.loads(user_manager.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)

        if len(sessions) > 5:
            sessions = sessions[-5:]

        user_manager.sessions = json.dumps(sessions)
        user_manager.save()

        self.set_cookie(self.settings["cookie_key_sess"],
            user_manager.email+":"+sess_key
        )
        self.redirect("/")

    def _list_form_keys(self):
        return ("login_name", "password")

    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_signin.html", form_data=form_data,
            form_errors=form_errors
        )

# /signout/
class AdminSignoutHandler(SiteBaseHandler):
    @tornado.web.addslash
    def get(self):
        self.clear_cookie(self.settings["cookie_key_sess"])
        self.redirect("/signin")


class RegisterForm(object):
    def __init__(self):
        self.member_name = {'re':"^.{0,15}$", 'msg':'长度不超过15'}
        self.email = {'re':"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", 'msg':'邮箱格式不正确'}
        self.password = {'re':"^.{0,30}$", 'msg':'密码长度不超过30'}
        self.password2 = {'re':"^.{0,30}$", 'msg':'密码长度不超过30'}
    
    def check_valid(self, form_data):
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
            return_data['error_msg'] = {'password':'密码不能为空'}
        elif not form_data.get('member_name'):
            return_data['error_msg'] = {'member_name':'昵称不能为空'}
        elif not form_data.get('email'):
            return_data['error_msg'] = {'email':'邮箱不能为空'}
        if return_data['error_msg']:
            return_data['status'] = False
            return return_data
        for key, regular in form_dict.items():
            post_value = form_data.get(key)
            # 让提交的数据 和 定义的正则表达式进行匹配
            ret = re.match(regular['re'], post_value)
            if not ret:
                return_data['status'] = False
                return_data['error_msg'] = {key:regular['msg']}
                return return_data
            clear_data[key] = post_value
        else:
            return_data['clear_data'] = clear_data
            return return_data
        

# /register/
class AdminRegisterHandler(SiteBaseHandler):
    def get(self):
        self._render()
    
    def post(self):
        form_data =  self._build_form_data()
        obj = RegisterForm()
        return_data = obj.check_valid(form_data)
        if return_data['error_msg']:
            self._render(form_data, return_data['error_msg'])
            return
        clear_data = return_data.get('clear_data')
        haspwd = hashlib.md5(clear_data['password'].encode(encoding='utf8')).hexdigest()
        clear_data['password'] = haspwd
        clear_data.update({'sessions':json.dumps(list()),
                            'status':'1',
                            'role':'admin',
                            'create_time':dt.datetime.now()})
        Member.create(**clear_data)
        return self.render("admin/a_register_success.html")
    
    def _list_form_keys(self):
        return ("member_name", "email", "password", "password2")

    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_register.html", form_data=form_data,
            form_errors=form_errors
        )


class ChangePasswordForm(object):
    def __init__(self):
        self.password = {'re':"^.{0,30}$", 'msg':'密码长度不超过30'}
        self.password2 = {'re':"^.{0,30}$", 'msg':'密码长度不超过30'}
        
    def check_valid(self, form_data):
        form_dict = self.__dict__
        clear_data = {}
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        
        if not form_data.get('password') or not form_data.get('password2'):
            return_data['error_msg'] = {'password':'密码不能为空'}
        if return_data['error_msg']:
            return_data['status'] = False
            return return_data
        for key, regular in form_dict.items():
            post_value = form_data.get(key)
            # 让提交的数据 和 定义的正则表达式进行匹配
            ret = re.match(regular['re'], post_value)
            if not ret:
                return_data['status'] = False
                return_data['error_msg'] = {key:regular['msg']}
                return return_data
            clear_data[key] = post_value
        else:
            return_data['clear_data'] = clear_data
            return return_data


# /change_password/
class AdminChangePasswordHandler(SiteBaseHandler):
    def get(self):
        self._render()
    
    def post(self):
        form_data =  self._build_form_data()
        obj = ChangePasswordForm()
        return_data = obj.check_valid(form_data)
        if return_data['error_msg']:
            self._render(form_data, return_data['error_msg'])
            return
        clear_data = return_data.get('clear_data')
        print(clear_data)
        old_haspwd = hashlib.md5(clear_data['password'].encode()).hexdigest()
        new_haspwd = hashlib.md5(clear_data['password2'].encode()).hexdigest()
        if bcrypt.hashpw(old_haspwd.encode('utf8'), self.current_user.hash_pwd.encode('utf8')) == self.current_user.hash_pwd.encode('utf8'):
            hashd = bcrypt.hashpw(new_haspwd.encode('utf8'), bcrypt.gensalt())
            Member.update_pwd(self.current_user.member_id, hashd)
            self.redirect('/signout/')
        else:
            return_data['error_msg'] = {'password':'密码错误'}
            self._render({}, return_data['error_msg'])
            return
        
    
    def _list_form_keys(self):
        return ("password", "password2")

    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_change_password.html", form_data=form_data,
            form_errors=form_errors
        )

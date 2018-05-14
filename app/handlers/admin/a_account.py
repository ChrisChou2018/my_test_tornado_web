
from app.libs import handlers
from app.models import member_model
import bcrypt
import random
import string
import time
import datetime as dt
import json
import tornado.web
import re


# /signin/
class AdminSigninHandler(handlers.SiteBaseHandler):
    def get(self):
        self._render()

    def post(self):
        form_data = self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return

        # Update the storage of password.
        member_obj = member_model.Member.get_member_by_login(form_data["login_name"])
        if not member_obj:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return
        pass_word = form_data["password"]
        salt_key = str(member_obj.salt_key)
        member_hashpw = str(member_obj.hash_pwd)
        signin_flag = False
        if member_hashpw:
            if bcrypt.hashpw((pass_word+salt_key).encode(),
                    member_hashpw.encode()) == member_hashpw.encode():
                signin_flag = True
        if not signin_flag:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return
        sess_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
            for i in range(10)
        )
        session = {"id":sess_key, "time":int(time.time())}
        try:
            sessions = json.loads(member_obj.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)
        if len(sessions) > 5:
            sessions = sessions[-5:]
        member_obj.sessions = json.dumps(sessions)
        member_obj.save()
        self.set_cookie(self.settings["cookie_key_sess"],
            member_obj.email+":"+sess_key
        )
        self.redirect("/")

    def _list_form_keys(self):
        return ("login_name", "password")

    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_signin.html", form_data=form_data,
            form_errors=form_errors
        )

# /signout/
class AdminSignoutHandler(handlers.SiteBaseHandler):
    @tornado.web.addslash
    def get(self):
        self.clear_cookie(self.settings["cookie_key_sess"])
        self.redirect("/signin")




# /register/
class AdminRegisterHandler(handlers.SiteBaseHandler):
    """
    用户注册页面
    """
    def get(self):
        self._render()
    
    def post(self):
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        member = member_model.Member
        form_data =  self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return
        clear_data = form_data
        member_obj_by_email, member_obj_by_name = (member.get_member_by_email(clear_data.get('email')), 
                                                member.get_member_by_member_name(clear_data.get('member_name')))
        if member_obj_by_email:
            return_data['error_msg']['has_member_error'] = '邮箱已经被注册'
        elif member_obj_by_name:
            return_data['error_msg']['has_member_error'] = '用户名已经存在'
        if return_data['error_msg']:
            self._render(form_data, return_data['error_msg'])
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
        return self.render("admin/a_register_success.html")
    
    def _list_form_keys(self):
        return ("member_name", "email", "password", "password2")

    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_register.html", form_data=form_data,
            form_errors=form_errors
        )
    
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


# /change_password/
class AdminChangePasswordHandler(handlers.SiteBaseHandler):
    """
    用户修改密码页面
    """
    def get(self):
        self._render()
    
    def post(self):
        form_data =  self._build_form_data()
        form_errors = self._validate_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return
        clear_data = form_data
        old_haspwd = clear_data['password']
        salt_key = self.current_user.salt_key
        new_haspwd = clear_data['password2']
        new_salt_key = ''.join(random.choice(string.ascii_lowercase + string.digits) \
            for i in range(8)
        )
        if bcrypt.hashpw((old_haspwd + salt_key).encode('utf8'), 
                        self.current_user.hash_pwd.encode('utf8')) == self.current_user.hash_pwd.encode('utf8'):
            hashd = bcrypt.hashpw((new_haspwd + new_salt_key).encode('utf8'), bcrypt.gensalt())
            member_model.Member.update_pwd(self.current_user.member_id, hashd)
            query = (member_model.Member
                .update({'salt_key':new_salt_key})
                .where(member_model.Member.member_id == self.current_user.member_id))
            query.execute()
            self.redirect('/signout/')
        else:
            form_errors.update({'password':'密码错误'})
            self._render({}, form_errors)
            return
        
    
    def _list_form_keys(self):
        return ("password", "password2")


    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_change_password.html", form_data=form_data,
            form_errors=form_errors
        )

    def _validate_form_data(self, form_data):
        form_errors = dict()
        for key in self._list_form_keys():
            if not form_data[key]:
                form_errors[key] = "不能为空"
        if form_data['password'] != form_data['password2']:
            form_errors['password'] = "两次密码不一致"
        if len(form_data['password']) > 30:
            form_errors['password'] = '密码长度不超过30'
        return form_errors
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import string
import random
import hashlib
import uuid
from datetime import *
import time

import bcrypt
import tornado.web

from app.libs.handlers import SiteBaseHandler


# /signin
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
        user_manager = UserManager.get_user_by_login(form_data["login_name"])
        if not user_manager:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return

        md5d = hashlib.md5(form_data["password"]).hexdigest()
        user_hashpw = str(user_manager.user_hashpw)
        user_pwd = user_manager.user_pwd

        signin_flag = False
        if user_hashpw:
            if bcrypt.hashpw(md5d, user_hashpw) == user_hashpw:
                signin_flag = True
        elif user_pwd:
            if md5d == user_pwd:
                signin_flag = True
                hashd = bcrypt.hashpw(md5d, bcrypt.gensalt())
                user_manager.user_hashpw = hashd
                user_manager.user_pwd = ""

        if not signin_flag:
            form_errors["form"] = "用户名/密码不匹配"
            self._render(form_data, form_errors)
            return

        sess_key = ''.join(random.choice(string.lowercase + string.digits) \
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
            user_manager.user_id+":"+sess_key
        )

        self.redirect("/")

    def _list_form_keys(self):
        return ("login_name", "password")

    def _render(self, form_data=None, form_errors=None):
        self.render("admin/a_signin.html", form_data=form_data,
            form_errors=form_errors
        )

# /signout
class AdminSignoutHandler(SiteBaseHandler):
    @tornado.web.addslash
    def get(self):
        self.clear_cookie(self.settings["cookie_key_sess"])
        self.redirect("/signin")


urls = [
    (r"/signin", AdminSigninHandler),
    (r"/signout/", AdminSignoutHandler),
]


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import parse
from urllib.parse import urlencode
import functools
from app.libs import data
from app.models.member_model import Member
import json


def admin_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user or not self.current_user.role:
            self.redirect("/signin")
            return
        return method(self, *args, **kwargs)
    return wrapper


def js_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user or not self.current_user.role:
            self.data['result'] = False
            self.data['message'] = '没有登录或者没有权限'
            self.write(json.dumps(self.data))
            return 
        return method(self, *args, **kwargs)
    return wrapper


def www_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "POST", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if parse.urlsplit(url).scheme:
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
        return method(self, *args, **kwargs)
    return wrapper


def api_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            member_id = self.get_argument("MemberId", None)
            return_data = dict()
            if not member_id:
                return_data["message"] = "你没有登陆"
                return_data["status"] = "session_error"
                self.write(return_data)
                return
        return method(self, *args, **kwargs)
    return wrapper

def has_permission(permission):
    def _has_permission(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            has_per = False
            if not self.current_user or not self.current_user.role:
                self.redirect("/signin")
                return
            if self.current_user.role not in data.roles:
                self.send_error(403)
                return
            # if self.current_user.user_name not in data.member_role[self.current_user.role]:
            #     self.send_error(403)
            #     return
            for each in data.role_permission[self.current_user.role]:
                if permission in data.permission_dict[each]:
                    has_per = True
            if not has_per:
                self.send_error(403)
                return
            return method(self, *args, **kwargs)
        return wrapper
    return _has_permission


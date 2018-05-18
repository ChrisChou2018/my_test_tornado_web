#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import tornado.web
import tornado.log

import config_web
import app.libs.data as lib_data
# import app.libs.picture as lib_picture
import app.models.base_model as base_model
from app.models.member_model import Member
import app.libs.common as lib_common


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client_version = ""
        self.platform = ""
        self.user_agent = ""
        if "User-Agent" in self.request.headers:
            self.user_agent = self.request.headers["User-Agent"]
            user_agent = self.request.headers["User-Agent"].split(" ")
            if user_agent and "Meihuishuo" in user_agent[0]:
                self.client_version = user_agent[0].replace("Meihuishuo/", "")
                if "Android" in self.user_agent:
                    self.platform = "Android"
                if "iOS" in self.user_agent:
                    self.platform = "iOS"
        if self.client_version:
            self.client_version_num = int(self.client_version.replace(".", ""))
        else:
            self.client_version_num = 0
        if "X-Forwarded-For" in self.request.headers:
            self.client_ip = self.request.headers["X-Forwarded-For"]
        elif "X-Real-Ip" in self.request.headers:
            self.client_ip = self.request.headers["X-Real-Ip"]
        else:
            self.client_ip = self.request.remote_ip
        self.request.remote_ip = self.client_ip

    def set_default_headers(self):
        self.set_header("Server", "mhs/1.0.1")

    def _list_form_keys(self):
        return list()

    def build_photo_url(self, photo_id, pic_version="title", pic_type="photos", cdn=False):
        return lib_common.build_photo_url(photo_id, pic_version, pic_type, cdn)

    def build_country_img_url(self, img_name):
        return lib_common.build_country_img_url(img_name)

    def build_apk_url(self, file_name):
        return lib_common.build_apk_url(file_name)

    def build_assets_url(self, filename, image=False):
        """构建静态文件url"""
        return lib_common.build_assets_url(filename, image)

    def write(self, chunk):
        if config_web.settings['debug'] and isinstance(chunk, dict):
            tornado.log.access_log.info(chunk)
        super(BaseHandler, self).write(chunk)


class DbBaseHandler(BaseHandler):
    def prepare(self):
        base_model.db_obj.connect()
        return super(DbBaseHandler, self).prepare()

    def on_finish(self):
        if not base_model.db_obj.is_closed():
            base_model.db_obj.close()
        return super(DbBaseHandler, self).on_finish()


class SiteBaseHandler(DbBaseHandler):
    def initialize(self):
        super(SiteBaseHandler, self).initialize()
        self.data = {"status":"error", "message":""}

    @property
    def site_name(self):
        return self.settings["site_name"]

    @property
    def next_url(self):
        next_url = self.get_argument("next", None)
        return next_url or "/"

    @property
    def start(self):
        start = self.get_argument("start", "0")
        return int(start) if start.isdigit() else 0

    def _build_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument("f_"+key, "")

        return form_data

    def _create_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")

        return form_data

    def _validate_form_data(self, form_data):
        form_errors = dict()
        for key in self._list_form_keys():
            if not form_data[key]:
                form_errors[key] = "不能为空"

        return form_errors

    def get_current_user(self):
        cookie_data = self.get_cookie(self.settings["cookie_key_sess"])
        if not cookie_data:
            return None

        try:
            member_id, session_id = cookie_data.split(":")
        except:
            return None

        member = Member.get_user_by_sess(member_id, session_id)
        return member


class WwwBaseHandler(DbBaseHandler):
    LOGIN_NEXT = "__next__"

    def prepare(self):
        #
        # 处理登录跳转
        #
        self._save_next_url()

    def initialize(self):
        super(WwwBaseHandler, self).initialize()
        self.data = {"status": "error", "message": ""}

    @property
    def site_name(self):
        return self.settings["site_name"]

    @property
    def next_url(self):
        next_url = self.get_argument("next", None)
        return next_url or "/"

    def _save_next_url(self):
        #
        # 保存 login_url 页面的 next 参数，以便登录后跳回。
        #
        if self.request.path == self.get_login_url():
            next = self.get_argument("next", None) or "/"
            self.set_secure_cookie(self.LOGIN_NEXT, next, expires_days = None)

    @property
    def start(self):
        start = self.get_argument("start", "0")
        return int(start) if start.isdigit() else 0

    def _build_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")

        return form_data

    def _create_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")

        return form_data

    def _validate_form_data(self, form_data):
        form_errors = dict()
        for key in self._list_form_keys():
            if not form_data[key]:
                form_errors[key] = "不能为空"

        return form_errors

    def get_current_user(self):
        cookie_data = self.get_cookie(self.settings["cookie_key_sess"])
        if not cookie_data:
            return None

        try:
            member_id, session_id = cookie_data.split(":")
        except:
            return None

        member = Member.get_user_by_sess(member_id, session_id)
        return member

    # def get_category(self):
    #     """get catagory
    #     """
    #     category_list = []
    #     parent_list = Type.list_type_by_parent_id(parent_id="0")
    #     for parent in parent_list:
    #         # sub_type_list = Type.list_type_by_parent_id(parent_id=parent.uuid)
    #         category = {}
    #         category["id"] = parent.uuid
    #         category["name"] = parent.title
    #         category["children"] = []
    #         # for sub_type in sub_type_list:
    #         #     grandson_type_list = Type.list_type_by_parent_id(query_set=sub_type_list,
    #         #                                                      parent_id=sub_type.uuid)
    #         #     children = {}
    #         #     children["id"] = sub_type.uuid
    #         #     children["name"] = sub_type.title
    #         #     children["children"] = []
    #         #     for grandson_type in grandson_type_list:
    #         #         children["children"].append({"id": grandson_type.uuid,
    #         #                                     "name": str(grandson_type.title)})
    #         #     category["children"].append(children)
    #         category_list.append(category)

    #     return category_list


class MobileBaseHandler(SiteBaseHandler):
    def get_current_user(self):
        if not 'Auth' in self.request.headers:
            return None

        auth = self.request.headers['Auth']
        member_id, session_id = auth.split(":")

        if not member_id or not session_id:
            return None

        member = Member.get_user_by_sess(member_id, session_id)
        return member


class JsWwwBaseHandler(WwwBaseHandler):
    def initialize(self):
        super(JsWwwBaseHandler, self).initialize()
        self.data = {"result": "error"}

    def _build_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")

        return form_data


class JsSiteBaseHandler(SiteBaseHandler):
    def initialize(self):
        super(SiteBaseHandler, self).initialize()
        self.data = {"result":"error"}

    def _build_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")

        return form_data


# api base handler
class ApiBaseHandler(DbBaseHandler):
    def initialize(self):
        super(ApiBaseHandler, self).initialize()
        self.data = {"status": "error", "message": ""}

    def check_xsrf_cookie(self):
        pass

    def _build_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")
        return form_data

    def _validate_form_data(self, form_data):
        form_errors = dict()
        for key in self._list_form_keys():
            if not form_data[key]:
                form_errors[key] = "不能为空"

        return form_errors

    def _return_data(self, return_data):
        return_mesage = dict()
        return_mesage["result"] = return_data

        return return_mesage

    def get_current_user(self):
        try:
            session_data = self.request.headers['Authorization']
        except Exception as e:
            session_data = None

        if not session_data:
            return None

        try:
            member_id, session_id = session_data.split(":")
        except:
            return None

        member = Member.get_user_by_sess(member_id, session_id)
        return member


    # def _upload_photo(self, picture_type="avatar"):
    #     pic_dict = dict()
    #     if not self.request.body:
    #         return pic_dict

    #     pic_dict = lib_picture.save_upload_picture(
    #         self.request.body, self.settings["static_path"],
    #         picture_type=picture_type, is_api=True
    #     )
    #     return pic_dict


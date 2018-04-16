#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import hashlib
import tornado.web

from meihuishuo.libs.handlers import ApiBaseHandler
from meihuishuo.models.util_model import Versions


# /v1/update_check
class ApiAppVersionsHandler(ApiBaseHandler):
    def get(self):
        self.data["status"] = "success"
        platform = "Android"

        if 'iOS' in self.request.headers["User-Agent"]:
            platform = "iOS"

        version = Versions.load_version(platform)

        if not version:
            self.data["status"] = "error"
            self.write(self.data)
            return

        self.data["update_content"] = version.update_content
        self.data["version_name"] = version.version_name
        self.data["version_code"] = version.version_code
        self.data["apk_md5"] = version.apk_md5
        self.data["apk_url"] = self.build_apk_url(version.file_name)

        self.write(self.data)


urls = [
    (r"/v1/update_check?", ApiAppVersionsHandler),
]

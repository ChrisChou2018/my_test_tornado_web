#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import peewee
import tornado.web
import tornado.log
import tornado.ioloop
import tornado.options
from tornado.options import define, options

import config_web
import app.handlers
import app.models.base_model as base_model
import app.libs.common as lib_common
from app.libs.url_include import url_wrapper, include
from app import models
from app.handlers import admin

define("port", default=9900)
define("debug", default=True)
define("smode", default="debug")
tornado.options.parse_command_line()
ui_modules = dict()
ui_modules.update(admin.ui_modules)
config_web.settings["ui_modules"] = ui_modules


class BaseApplication(tornado.web.Application):
    def log_request(self, handler):
        log_method = tornado.log.access_log.error
        if handler.get_status() < 400:
            log_method = tornado.log.access_log.info
        elif handler.get_status() < 500:
            log_method = tornado.log.access_log.warning

        request_time = 1000.0 * handler.request.request_time()
        request_summary = "%s %s (%s)" % (handler.request.method, handler.request.uri,
                                          handler.request.remote_ip)
        log_method("%d %s %.2fms", handler.get_status(),
                   request_summary, request_time)


app = BaseApplication(
    [],
    **config_web.settings
)
app.add_handlers(config_web.settings["admin_domain"], admin.urls)

def main():
    app.listen(options.port, address="127.0.0.1", xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

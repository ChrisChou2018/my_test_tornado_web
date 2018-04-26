#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import peewee
import tornado.web
import tornado.log
import tornado.ioloop
import tornado.options
import config_web
import app.handlers
# import app.handlers.www.w_footer
# import app.handlers.www.w_callback
import app.models.base_model as base_model
import app.libs.common as lib_common
from tornado.options import define, options
from app.libs.url_include import url_wrapper, include
from app.handlers.admin.ui_modules import ui_modules as ui_modules_dict
from app.handlers.api import urls as api_admin_urls
from app.handlers.admin import urls as admin_urls

define("port", default=9900)
define("debug", default=True)
define("smode", default="debug")


tornado.options.parse_command_line()

ui_modules = dict()
ui_modules.update(ui_modules_dict)
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


# urls = [
#         ('/admin',              include('app.handlers.admin.urls'),),
#     ]

app = BaseApplication(
    [],
    # url_wrapper(urls),  #url_wrapper 检索列表中的元素元素类型如果是include倒入的列表类型将其实现路径拼接如:/admin/signin/
    **config_web.settings
    )
app.add_handlers(config_web.settings["admin_domain"], admin_urls)
app.add_handlers(config_web.settings["admin_domain"], api_admin_urls)
# base_model.setup_db_obj()
# lib_common.assets_map()


def main():
    app.listen(options.port, address="127.0.0.1", xheaders=True)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    main()

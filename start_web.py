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
import app.handlers.admin.a_account
import app.handlers.www.w_footer
# import app.handlers.www.w_callback
import app.models.base_model as base_model
import app.libs.common as lib_common
from tornado.options import define, options
from importlib import import_module

define("port", default=9900)
define("debug", default=True)
define("smode", default="debug")
urls = list()
admin_urls = list()
admin_urls.extend(app.handlers.admin.a_account.urls)
admin_urls.extend(app.handlers.ADMIN_EXT_URLS)
# www_urls = list()
# www_urls.extend(app.handlers.www.w_index.urls)
# www_urls.extend(app.handlers.www.w_goods.urls)
# www_urls.extend(app.handlers.www.w_account.urls)
# www_urls.extend(app.handlers.www.w_order.urls)
# www_urls.extend(app.handlers.www.w_coupon.urls)
# m_urls = list()
# m_urls.extend(app.handlers.mobile.m_invite.urls)
# m_urls.extend(app.handlers.mobile.m_share.urls)
# m_urls.extend(app.handlers.mobile.m_activities.urls)
# m_urls.extend(app.handlers.mobile.m_index.urls)
# m_urls.extend(app.handlers.mobile.m_goods.urls)
# m_urls.extend(app.handlers.mobile.m_account.urls)


tornado.options.parse_command_line()

def include(module):
    res = import_module(module)
    urls = getattr(res, 'urls', res)
    return urls

def url_wrapper(urls):
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles, (tuple, list)):
            for handle in handles:
                pattern, handle_class = handle
                wrap = ('{0}{1}'.format(path, pattern), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list


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
    url_wrapper([
        ('/admin', include('app.handlers.admin.urls'),),
        ]),
    **config_web.settings)
# app.add_handlers(config_web.settings["admin_domain"], admin_urls)

# base_model.setup_db_obj()
# lib_common.assets_map()


def main():
    app.listen(options.port, address="127.0.0.1", xheaders=True)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

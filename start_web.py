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
import app.handlers.admin.a_welcome
import app.handlers.admin.a_account
import app.handlers.admin.a_orders
import app.handlers.admin.a_brands
import app.handlers.admin.a_goods
import app.handlers.admin.a_warehouse
import app.handlers.admin.a_limited
import app.handlers.admin.a_home
import app.handlers.admin.a_versions
import app.handlers.admin.a_coupons
import app.handlers.admin.a_user_manager
import app.handlers.admin.a_category
import app.handlers.admin.a_activities
import app.handlers.admin.a_members
import app.handlers.admin.a_feedbacks
import app.handlers.admin.a_metadatas
import app.handlers.admin.a_articles
import app.handlers.admin.a_push
import app.handlers.admin.a_skin_tests
import app.handlers.admin.a_staff_goods
import app.handlers.api.api_welcome
import app.handlers.api.api_callback
import app.handlers.api.api_account
import app.handlers.api.api_goods
import app.handlers.api.api_order
import app.handlers.api.api_home
import app.handlers.api.api_activities
# import meihuishuo.handlers.api.api_member
import app.handlers.api.api_suggestion_type
import app.handlers.api.api_versions
import app.handlers.api.api_coupon
import app.handlers.api.api_category
# import app.handlers.api.api_activities
import app.handlers.api.api_articles
import app.handlers.api.api_skin_tests
import app.handlers.mobile.m_invite
import app.handlers.mobile.m_share
import app.handlers.mobile.m_activities
import app.handlers.mobile.m_index
import app.handlers.mobile.m_goods
import app.handlers.mobile.m_account
import app.handlers.mobile.m_cart
import app.handlers.mobile.m_order
import app.handlers.mobile.m_coupon
import app.handlers.mobile.m_address
import app.handlers.mobile.m_about
import app.handlers.mobile.m_articles
import app.handlers.mobile.m_skintest
import app.handlers.mobile.m_check_in
import app.handlers.mobile.m_ubskin
import app.handlers.www.w_index
import app.handlers.www.w_goods
import app.handlers.www.w_account
import app.handlers.www.w_order
import app.handlers.www.w_coupon
import app.handlers.www.w_search
import app.handlers.www.w_cart
import app.handlers.www.w_user
import app.handlers.www.w_order_confirm
import app.handlers.www.w_advertisement
import app.handlers.www.w_footer
import app.handlers.www.w_product
import app.handlers.www.w_articles
import app.handlers.www.w_callback
import app.handlers.www.w_staff
import app.handlers.stat.s_stat
import app.handlers.stat.s_account

import app.models.base_model as base_model
import app.libs.common as lib_common

from tornado.options import define, options


define("port", default=9900)
define("debug", default=True)
define("smode", default="debug")


urls = list()
admin_urls = list()
admin_urls.extend(app.handlers.admin.a_welcome.urls)
admin_urls.extend(app.handlers.admin.a_account.urls)
admin_urls.extend(app.handlers.admin.a_orders.urls)
admin_urls.extend(app.handlers.admin.a_brands.urls)
admin_urls.extend(app.handlers.admin.a_goods.urls)
admin_urls.extend(app.handlers.admin.a_warehouse.urls)
admin_urls.extend(app.handlers.admin.a_limited.urls)
admin_urls.extend(app.handlers.admin.a_home.urls)
admin_urls.extend(app.handlers.admin.a_versions.urls)
admin_urls.extend(app.handlers.admin.a_coupons.urls)
admin_urls.extend(app.handlers.admin.a_user_manager.urls)
admin_urls.extend(app.handlers.admin.a_category.urls)
admin_urls.extend(app.handlers.admin.a_activities.urls)
admin_urls.extend(app.handlers.admin.a_members.urls)
admin_urls.extend(app.handlers.admin.a_feedbacks.urls)
admin_urls.extend(app.handlers.admin.a_metadatas.urls)
admin_urls.extend(app.handlers.admin.a_articles.urls)
admin_urls.extend(app.handlers.admin.a_push.urls)
admin_urls.extend(app.handlers.admin.a_skin_tests.urls)
admin_urls.extend(app.handlers.admin.a_staff_goods.urls)
admin_urls.extend(app.handlers.ADMIN_EXT_URLS)
api_urls = list()
api_urls.extend(app.handlers.api.api_welcome.urls)
api_urls.extend(app.handlers.api.api_callback.urls)
api_urls.extend(app.handlers.api.api_account.urls)
api_urls.extend(app.handlers.api.api_goods.urls)
api_urls.extend(app.handlers.api.api_order.urls)
api_urls.extend(app.handlers.api.api_home.urls)
api_urls.extend(app.handlers.api.api_activities.urls)
# api_urls.extend(app.handlers.api.api_shop.urls)
api_urls.extend(app.handlers.api.api_shop_cart.urls)
# api_urls.extend(app.handlers.api.api_member.urls)
api_urls.extend(app.handlers.api.api_suggestion_type.urls)
api_urls.extend(app.handlers.api.api_versions.urls)
api_urls.extend(app.handlers.api.api_coupon.urls)
api_urls.extend(app.handlers.api.api_category.urls)
api_urls.extend(app.handlers.api.api_articles.urls)
api_urls.extend(app.handlers.api.api_skin_tests.urls)
m_urls = list()
m_urls.extend(app.handlers.mobile.m_invite.urls)
m_urls.extend(app.handlers.mobile.m_share.urls)
m_urls.extend(app.handlers.mobile.m_activities.urls)
m_urls.extend(app.handlers.mobile.m_index.urls)
m_urls.extend(app.handlers.mobile.m_goods.urls)
m_urls.extend(app.handlers.mobile.m_account.urls)
m_urls.extend(app.handlers.mobile.m_cart.urls)
m_urls.extend(app.handlers.mobile.m_order.urls)
m_urls.extend(app.handlers.mobile.m_coupon.urls)
m_urls.extend(app.handlers.mobile.m_address.urls)
m_urls.extend(app.handlers.mobile.m_about.urls)
m_urls.extend(app.handlers.mobile.m_articles.urls)
m_urls.extend(app.handlers.mobile.m_skintest.urls)
m_urls.extend(app.handlers.mobile.m_check_in.urls)
m_urls.extend(app.handlers.mobile.m_ubskin.urls)
www_urls = list()
www_urls.extend(app.handlers.www.w_index.urls)
www_urls.extend(app.handlers.www.w_goods.urls)
www_urls.extend(app.handlers.www.w_account.urls)
www_urls.extend(app.handlers.www.w_order.urls)
www_urls.extend(app.handlers.www.w_coupon.urls)
www_urls.extend(app.handlers.www.w_search.urls)
www_urls.extend(app.handlers.www.w_cart.urls)
www_urls.extend(app.handlers.www.w_user.urls)
www_urls.extend(app.handlers.www.w_order_confirm.urls)
www_urls.extend(app.handlers.www.w_advertisement.urls)
www_urls.extend(app.handlers.www.w_footer.urls)
www_urls.extend(app.handlers.www.w_product.urls)
www_urls.extend(app.handlers.www.w_articles.urls)
www_urls.extend(app.handlers.www.w_callback.urls)
www_urls.extend(app.handlers.www.w_staff.urls)
stat_urls = list()
stat_urls.extend(app.handlers.stat.s_stat.urls)
stat_urls.extend(app.handlers.stat.s_account.urls)

ui_modules = dict()
ui_modules.update(app.handlers.admin.a_welcome.ui_modules)
# ui_modules.update(app.handlers.a_front.ui_modules)


tornado.options.parse_command_line()
config_web.settings["ui_modules"] = ui_modules

# settings = config_web.settings_common
# settings["ui_modules"] = ui_modules
# if options.smode == "debug":
#     settings.update(config_web.settings_debug)
# elif options.smode == "testing":
#     settings.update(config_web.settings_testing)
# else:
#     settings.update(config_web.settings_online)


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


app = BaseApplication(urls, **config_web.settings)
app.add_handlers(config_web.settings["admin_domain"], admin_urls)
app.add_handlers(config_web.settings["api_domain"], api_urls)
app.add_handlers(config_web.settings["m_domain"], m_urls)
app.add_handlers(config_web.settings["www_domain"], www_urls)
app.add_handlers(config_web.settings["stat_domain"], stat_urls)

# base_model.setup_db_obj()
lib_common.assets_map()


def main():
    app.listen(options.port, address="127.0.0.1", xheaders=True)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

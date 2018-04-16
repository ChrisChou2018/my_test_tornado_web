#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import peewee
import tornado.web
import tornado.testing

import config_web

from tornado.options import define, options

import meihuishuo.models.base_model as base_model


CURR_ROOT = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.join(CURR_ROOT, "..", "..")


class BaseHTTPTestCase(tornado.testing.AsyncHTTPTestCase):
    def __init__(self, methodName='runTest', **kwargs):
        super(BaseHTTPTestCase, self).__init__(methodName, **kwargs)

    def setUp(self):
        super(BaseHTTPTestCase, self).setUp()

    def get_app(self):
        settings = config_web.settings_common
        settings.update(config_web.settings_testing)
        # config_file_path = os.path.join(APP_ROOT, "conf", "app_testing.cfg")
        # tornado.options.parse_config_file(config_file_path)

        self.app = tornado.web.Application(list(), **settings)
        self.app.db_obj = peewee.MySQLDatabase(config_web.db_name, host=config_web.db_host,
            port=config_web.db_port, user=config_web.db_user, password=config_web.db_pass
        )
        base_model.setup_db_obj(self.app.db_obj)
        self.set_handlers()
        return self.app

    def get_handlers(self):
        raise NotImplementedError()

    def set_handlers(self):
        raise NotImplementedError()

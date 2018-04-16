#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import textwrap
import unittest
import tornado.web
import tornado.ioloop
import tornado.testing
import tornado.options
import tornado.httpserver

from tornado.options import define, options
import app.tests.test_api_orders


define("debug", default=True, group="app")
define("autoreload", default=False, group="app")

define("xsrf_cookies", default=False, group="app")
define("cookie_secret", default="", group="app")
define("db_name", default="", group="app")

options.logging = "warning"


class BaseTextTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super(BaseTextTestRunner, self).run(test)
        if result.skipped:
            skip_reasons = set(reason for (test, reason) in result.skipped)
            self.stream.write(textwrap.fill(
                "Some tests were skipped because: %s" %
                ", ".join(sorted(skip_reasons)))
            )
            self.stream.write("\n")
        return result


TEST_MODULES = [
    # "app.tests.test_api_orders",
    # "app.tests.test_api_account",
    # "app.tests.test_api_goods",
    # "app.tests.test_api_home",
    # "app.tests.test_api_shop",
    "app.tests.test_api_shop_cart"
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


def main():
    # kwargs = {"testRunner":BaseTextTestRunner}
    # try:
    #     tornado.testing.main()
    #     print "ha?"
    # except:
    #     logging.exception("Error when start testing...")
    # finally:
    #     sys.exit(1)
    tornado.testing.main()


if __name__ == "__main__":
    main()

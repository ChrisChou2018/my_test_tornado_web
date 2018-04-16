#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

import app.lib.db_object as db_object

from app.lib.handlers import BaseHandler


# /
class HomeHandler(BaseHandler):
    def get(self):
        articles = db_object.list_article_by_cond(
            {"status":"normal"}, limit=10, is_strip_tags=True
        )
        self.render("index.html", articles=articles)


urls = [
    (r"/", HomeHandler),
]


class HeaderModule(tornado.web.UIModule):
    def render(self, tpl="m_header.html"):
        return self.render_string(tpl)


class FooterModule(tornado.web.UIModule):
    def render(self, tpl="m_footer.html"):
        return self.render_string(tpl)


ui_modules = {
    "HeaderModule" : HeaderModule,
    "FooterModule" : FooterModule,
}


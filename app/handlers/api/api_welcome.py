#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

# import webapp.lib.db_object as db_object
import meihuishuo.models.goods_model as goods_model

from meihuishuo.libs.handlers import ApiBaseHandler


# /
class ApiHomeHandler(ApiBaseHandler):
    def get(self):
        # articles = db_object.list_article_by_cond(
        #     {"status":"normal"}, limit=10, is_strip_tags=True
        # )
        # self.render("index.html", articles=articles)
        # self.set_header("Content-Type", "application/json; charset=UTF-8")
        # self.write("{\"test\":"+json.dumps("测试")+"}")
        # print goods_model.Goods._meta.database.get_tables()
        # for i in goods_model.Goods.select():
        #     print i

        # r = self.get_argument("r", None)

        # import meihuishuo.models.rq_model as rq_model

        # import meihuishuo.workers.wms_worker as wms_worker
        # order_data = {"order_id":"96361506799609", "warehouse_id":"d2edf46b-b961-4478-848f-c6698b3b2e1e"}
        # rq_model.enqueue_job(wms_worker.wms_push_order, order_data)

        import meihuishuo.models.member_model as member_model
        print member_model.change_account_balance('90cef741aaf04ef', 49, 'invite_vip')

        self.write("")


class ApiWxJsDomainTokenHandler(ApiBaseHandler):
    def get(self):
        self.write('8gewxfqo5p0FEfsj')


urls = [
    (r"/", ApiHomeHandler),
    (r'/MP_verify_8gewxfqo5p0FEfsj.txt', ApiWxJsDomainTokenHandler),
]

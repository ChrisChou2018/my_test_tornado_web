#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import meihuishuo.libs.data as data
import meihuishuo.models.goods_model as goods_model
import meihuishuo.models.order_model as order_model
import json
import datetime as dt

from peewee import fn, SQL
from meihuishuo.models.goods_model import HomeLimitedGoods, Goods, Comment
from meihuishuo.libs.handlers import SiteBaseHandler, ApiBaseHandler
from meihuishuo.libs.decorators import admin_authenticated


# /
class AdminHomeHandler(SiteBaseHandler):
    @admin_authenticated
    def get(self):
        month_days = {"1": 31, "2": 28, "3": 31, "4": 30, "5": 31, "6": 30,
            "7": 31, "8": 31, "9": 30, "10": 31, "11": 30, "12": 31
        }
        today = dt.date.today()
        if (today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)):
            month_days["2"] = 29

        week_ben_date = today - dt.timedelta(days=(today.weekday()+7))
        week_end_date = today - dt.timedelta(days=today.weekday()+1)
        last_month = today - dt.timedelta(days=today.day)
        month_ben_date = dt.datetime(last_month.year, last_month.month, 1, 0, 0)
        month_end_date = dt.datetime(last_month.year, last_month.month,
            month_days[str(last_month.month)], 23, 59, 59)
        day_order_stats = order_model.OrderStat.list_order_stats(limit_num=30, show=True)
        week_order_stats = order_model.OrderStat.list_order_stats(
            stat_type=["week"], limit_num=20, show=True)
        month_order_stats = order_model.OrderStat.list_order_stats(
            stat_type=["month"], limit_num=12, show=True)
        shop_order_stats = order_model.OrderStat.list_order_stats(
            limit_num=7, stat_type=["shop_sum"], show=True)
        shop_order_stats.reverse()
        week_shop_order_stats = order_model.OrderStat.list_order_stats_by_date(
            ben_date=str(week_ben_date)[0: 10], end_date=str(week_end_date)[0: 10],
            stat_type="shop_sum")
        month_shop_order_stats = order_model.OrderStat.list_order_stats_by_date(
            ben_date=str(month_ben_date)[0: 10], end_date=str(month_end_date)[0: 10],
            stat_type="shop_sum")
        week_stats = dict()
        month_stats = dict()
        for each in week_shop_order_stats:
            w_data = json.loads(each.data)
            for w_d in w_data:
                if w_d not in week_stats:
                    week_stats[w_d] = w_data[w_d]["price"]
                    continue

                week_stats[w_d] += w_data[w_d]["price"]

        for each in month_shop_order_stats:
            m_data = json.loads(each.data)
            for m_d in m_data:
                if m_d not in month_stats:
                    month_stats[m_d] = m_data[m_d]["price"]
                    continue

                month_stats[m_d] += m_data[m_d]["price"]

        self.render("admin/a_index.html", day_order_stats=day_order_stats,
            week_order_stats=week_order_stats, month_order_stats=month_order_stats,
            shop_names=data.shop_names, shop_order_stats=shop_order_stats,
            week_stats=week_stats, month_stats=month_stats)


# /j/add_job
class AdminJsAddJobHandler(ApiBaseHandler):
    def get(self):
        # import meihuishuo.models.rq_model as rq_model
        # import meihuishuo.workers.wms_worker as wms_worker
        # order_data = {"order_id":"32132132131", "warehouse_id":"1231231231"}
        # rq_model.enqueue_job(wms_worker.wms_push_order, order_data)

        import os
        import uuid
        from PIL import Image
        import meihuishuo.models.goods_model as goods_model
        import meihuishuo.libs.picture as lib_picture

        source_path = os.path.join(self.settings["static_path"], "..", "localfile")

        for goods_img in goods_model.GoodsImg.select().\
                where(goods_model.GoodsImg.img_view.contains(".")).limit(50):
            if "." in goods_img.img_view:
                self.write(goods_img.goods_id)
                self.write("<br/>")
                self.write(goods_img.img_view)
                self.write("<br/>")

                source_file_path = os.path.join(source_path, goods_img.img_view)
                if not os.path.isfile(source_file_path):
                    goods_model.GoodsImg.delete_goods_img_by_uuid(goods_img.uuid)
                    self.write("!!! FILE NOT EXISTS: " + source_file_path)
                    self.write("<br/>")
                    continue

                photo_id = uuid.uuid4().hex
                target_path = os.path.join(self.settings["static_path"],
                    "photos", "raw", photo_id[:2])
                if not os.path.exists(target_path):
                    os.makedirs(target_path, 0755)

                target_file_path = os.path.join(target_path, photo_id+".jpg")

                photo_obj = Image.open(source_file_path)
                try:
                    photo_obj.save(target_file_path)
                except:
                    self.write("CONVERT FAILED !!!")
                    self.write("<br/>")
                    goods_model.GoodsImg.delete_goods_img_by_uuid(goods_img.uuid)
                    continue

                self.write(source_file_path)
                self.write("<br/>")
                self.write(target_file_path)
                self.write("<br/>")

                lib_picture.convert_picture(
                    photo_id, self.settings["static_path"], source_file_path
                )
                goods_model.GoodsImg.update(img_view=photo_id). \
                    where(goods_model.GoodsImg.uuid==goods_img.uuid).execute()

        return

        for goods in goods_model.Goods.select().\
                where((goods_model.Goods.status!="99") & \
                    (goods_model.Goods.img_view.contains("."))).limit(10):
            if not goods.img_view:
                self.write("!!! EMPTY IMGVIEW: " + goods.goods_id)
                self.write("<br/>")
                continue

            if "." in goods.img_view:
                self.write(goods.goods_id)
                self.write("<br/>")

                source_file_path = os.path.join(source_path, goods.img_view)
                if not os.path.isfile(source_file_path):
                    self.write("!!! FILE NOT EXISTS: " + source_file_path)
                    continue

                photo_id = uuid.uuid4().hex
                target_path = os.path.join(self.settings["static_path"],
                    "photos", "raw", photo_id[:2])
                if not os.path.exists(target_path):
                    os.makedirs(target_path, 0755)

                target_file_path = os.path.join(target_path, photo_id+".jpg")

                photo_obj = Image.open(source_file_path)
                photo_obj.save(target_file_path)

                self.write(source_file_path)
                self.write("<br/>")
                self.write(target_file_path)

                lib_picture.convert_picture(
                    photo_id, self.settings["static_path"], source_file_path
                )
                goods_model.Goods.update_goods(goods.goods_id, {"img_view":photo_id})

                # photo_dict = lib_picture.convert_picture()

                # return


    def get1(self):
        import time
        from rq import Queue
        from redis import Redis
        from meihuishuo.workers.ems_worker import test_rq

        redis_conn = Redis()
        q = Queue(connection=redis_conn)

        job = q.enqueue(test_rq, "3")
        time.sleep(5)
        self.data["result"] = job.result
        # self.data["result"] = "success"
        self.write(self.data)


# /welcome/update_limited_goods_price/
class AdminUpdateLimitedGoodsPriceHandler(SiteBaseHandler):
    def post(self):
        """
        获取promo_goods表的最低价格
        更新goods表的current_price
        :return:
        """

        limited_goods = [each for each in HomeLimitedGoods.select().where((
            HomeLimitedGoods.status=="normal")&(HomeLimitedGoods.limited_status=="on")&(
            (HomeLimitedGoods.limited_start_at==None)|((
                fn.timestampdiff(SQL("MINUTE"),fn.now(),HomeLimitedGoods.limited_end_at) >= 0)&(
                fn.timestampdiff(SQL("MINUTE"),HomeLimitedGoods.limited_start_at, fn.now()) >= 0)
                ))).order_by(HomeLimitedGoods.goods_limited_price.asc())]

        goods_list = [each for each in Goods.select(Goods.goods_id, Goods.price,
            Goods.current_price).where(Goods.status != "99").dicts()
        ]

        for goods in goods_list:
            current_price = goods["price"]
            l_goods = None
            for l_g in limited_goods:
                if goods["goods_id"] == l_g.goods_id:
                    l_goods = l_g
                    break

            if l_goods and l_goods.goods_limited_price != goods["price"]:
                current_price = l_goods.goods_limited_price

            if current_price != goods["current_price"]:
                Goods.update_goods(goods["goods_id"], {"current_price":current_price})


class AdminUpdateGoodsCommentCountHandler(SiteBaseHandler):
    def post(self):
        """
        获取comment表里面所有的评论
        循环goods和comments，计算每个goods的comment_count
        更新goods的comment_count
        """
        goods_list = Goods.list_all_goods()
        comments = Comment.list_all_comments()
        goods = list()
        for each in goods_list:
            comment_count = 0
            for comment in comments:
                if each["goods_id"] == comment["goods_id"]:
                    comment_count += 1

            Goods.update_goods(each["goods_id"], {"comment_count": comment_count})

        self.write("success")


class AdminOrderStatGoodsDetailHandler(SiteBaseHandler):
    def get(self, order_stat_id):
        order_stat = order_model.OrderStat.load_order_stats_by_id(order_stat_id)
        if not order_stat:
            self.send_error(404)
            return

        o_goods = json.loads(order_stat.data)
        goods_uuids = [each[0] for each in o_goods if each]
        goods = {g.goods_uuid: g for g in \
            goods_model.Goods.list_goods_by_goods_uuids(goods_uuids)}

        stats = dict()
        o_stats = order_model.OrderStat.list_order_stats_by_date(
            order_stat.ben_date, order_stat.end_date)
        for o_s in o_stats:
            s_data = json.loads(o_s.data)
            for s_d in s_data:
                if s_d not in stats:
                    stats[s_d] = dict()
                    stats[s_d]["order_sum"] = s_data[s_d]["order_sum"]
                    stats[s_d]["price"] = s_data[s_d]["price"]
                    continue

                try:
                    stats[s_d]["order_sum"] += s_data[s_d]["order_sum"]
                    stats[s_d]["price"] += s_data[s_d]["price"]
                except Exception, e:
                    pass

        province_order_stats = order_model.OrderStat.list_order_stats_by_date(
            ben_date=order_stat.ben_date, end_date=order_stat.end_date,
            stat_type="province_sum"
        )
        pro_dict = dict()
        for pro in province_order_stats:
            pro_data = json.loads(pro.data)
            for d in pro_data:
                if d not in pro_dict:
                    pro_dict[d] = dict()
                    pro_dict[d]["order_sum"] = int(pro_data[d]["order_sum"])
                    pro_dict[d]["price"] = float(pro_data[d]["price"])
                    continue

                pro_dict[d]["order_sum"] += int(pro_data[d]["order_sum"])
                pro_dict[d]["price"] += float(pro_data[d]["price"])

        self.render("a_order_stats/a_goods_detail.html", goods=goods,
            order_goods=o_goods, stats=stats, shop_names=data.shop_names,
            provinces=data.provinces, province_stats=pro_dict)


class AdminOrderStatShopDetailHandler(SiteBaseHandler):
    def get(self):
        shop_id = self.get_argument("shop_id", "")
        if not shop_id:
            return

        day_order_stats = order_model.OrderStat.list_order_stats(
            limit_num=30, stat_type=["shop_sum"], show=True)
        days = []
        order_sum = []
        prices = []
        for index, each in enumerate(day_order_stats):
            days.append(str(each.ben_date))
            order_sum.append(0)
            prices.append(0)
            d_data = json.loads(each.data)
            for d in d_data:
                if d == shop_id:
                    order_sum[index] = d_data[d]["order_sum"]
                    prices[index] = d_data[d]["price"]
                    break

        province_order_stats = order_model.OrderStat.list_order_stats(
            limit_num=30, stat_type=["shop_province_sum"], show=True)
        province_stats = dict()
        for each in province_order_stats:
            p_data = json.loads(each.data)
            if shop_id in p_data:
                # province_stats = p_data[shop_id]
                for p in p_data[shop_id]:
                    if p not in province_stats:
                        province_stats[p] = dict()
                        province_stats[p]["order_sum"] = p_data[shop_id][p]["order_sum"]
                        province_stats[p]["price"] = p_data[shop_id][p]["price"]
                        continue

                    province_stats[p]["order_sum"] += p_data[shop_id][p]["order_sum"]
                    province_stats[p]["price"] += p_data[shop_id][p]["price"]

        goods_stats = order_model.OrderStat.list_order_stats(
            limit_num=30, stat_type=["shop_goods"], show=True)
        order_goods = dict()
        for each in goods_stats:
            g_data = json.loads(each.data)
            if shop_id in g_data:
                for g in g_data[shop_id]:
                    if g not in order_goods:
                        order_goods[g] = dict()
                        order_goods[g]["goods_count"] = g_data[shop_id][g]["goods_count"]
                        order_goods[g]["goods_name"] = g_data[shop_id][g]["goods_name"]
                        order_goods[g]["price"] = g_data[shop_id][g]["price"]
                        continue

                    order_goods[g]["goods_count"] += g_data[shop_id][g]["goods_count"]
                    order_goods[g]["price"] += g_data[shop_id][g]["price"]

        order_goods = sorted(order_goods.iteritems(), key=lambda d: d[1]["goods_count"], reverse=True)
        if len(order_goods) > 10:
            order_goods = order_goods[0: 10]

        for each in order_goods:
            each[1]["avg_price"] = round(each[1]["price"]/each[1]["goods_count"], 2)

        goods_uuids = [each[0] for each in order_goods if each]
        goods = {g.goods_uuid: g for g in \
            goods_model.Goods.list_goods_by_goods_uuids(goods_uuids)}

        self.render("a_order_stats/a_shop_stats.html", shop_stats={
            "days": days, "order_sum": order_sum, "prices": prices},
            province_stats=province_stats, provinces=data.provinces,
            order_goods=order_goods, goods=goods)


urls = [
    (r"/", AdminHomeHandler),
    (r"/j/add_job/?", AdminJsAddJobHandler),
    (r"/welcome/update_limited_goods_price/?", AdminUpdateLimitedGoodsPriceHandler),
    (r"/welcome/update_goods_comment_count/?", AdminUpdateGoodsCommentCountHandler),
    (r"/welcome/order_stat_goods/([a-z0-9-]+)/?", AdminOrderStatGoodsDetailHandler),
    (r"/welcome/order_stat_shop/?", AdminOrderStatShopDetailHandler),
]


class AdminNavModule(tornado.web.UIModule):
    def render(self, tpl="admin/a_m_nav.html"):
        return self.render_string(tpl)


class AdminMenuModule(tornado.web.UIModule):
    def render(self, module_name, tpl="admin/a_m_menu.html"):
        permissions = data.role_permission[self.current_user.role]
        return self.render_string(tpl, module_name=module_name,
            permissions=permissions
        )


class AdminFooterModule(tornado.web.UIModule):
    def render(self, tpl="admin/a_m_footer.html"):
        return self.render_string(tpl)


ui_modules = {
    "AdminNavModule": AdminNavModule,
    "AdminMenuModule": AdminMenuModule,
    "AdminFooterModule": AdminFooterModule,
}


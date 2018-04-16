# -*- coding: utf-8 -*-

import uuid
import re
import decimal
import math

import tornado.web
from datetime import datetime

from meihuishuo.libs.handlers import WwwBaseHandler
from meihuishuo.libs.decorators import www_authenticated
import meihuishuo.models.goods_model as goods_model
from meihuishuo.libs.pagination import Paginator


class WwwwStaffGoodsHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        if not self.current_user.is_staff:
            self.redirect("/")
            return

        category_list = self.get_category()
        num = 40
        goods_l = [each for each in goods_model.StaffGoods.list_goods(start=self.start,
                                                                      num=num, online=True)]
        goods_ids = [item.goods_id for item in goods_l]
        limited_goods = goods_model.list_goods_min_price(goods_ids, status="all_goods",
                                                         all_promo_goods=True)

        goods_list = []
        if limited_goods:
            for each in goods_l:
                for item in limited_goods:
                    if each.goods_id == item.goods_id:
                        goods_info = {}
                        goods_info["uuid"] = each.uuid
                        goods_info["goods_id"] = each.goods_id
                        goods_info["staff_price"] = each.price
                        goods_info["current_price"] = item.current_price
                        goods_info["domestic_price"] = item.domestic_price
                        goods_info["title"] = item.goods_title
                        goods_info["img_url"] = self.build_photo_url(item.img_view,
                                                                     pic_type="goods", cdn=True)
                        goods_info["stock"] = item.stock
                        goods_info["staff_stock"] = each.stock
                        goods_info["intro"] = item.goods_intro
                        goods_info["status"] = each.status
                        goods_info["buy_count"] = item.buy_count

                        if goods_info["stock"] < 1 or goods_info["staff_stock"] < 1:
                            goods_info["is_sold_out"] = 1
                        else:
                            goods_info["is_sold_out"] = 0

                        if self.current_user:
                            member_id = self.current_user.member_id
                            collection_count = goods_model.Collection.get_colletion_id_count(member_id, item.goods_id)
                            if collection_count:
                                goods_info["is_favorite"] = "1"
                            else:
                                goods_info["is_favorite"] = "0"
                        else:
                            goods_info["is_favorite"] = "0"

                        goods_list.append(goods_info)

        goods_count = goods_model.StaffGoods.list_goods(online=True, is_count=True)

        # 分页
        paginator = Paginator(goods_count, num)
        page = paginator.page(self.start/num+1)
        pages = paginator.calculate_display_pages(1)
        page_num = paginator.total_pages
        less_than_certain_size = paginator.check_less_than_certain_size()
        page_args = {"page": page, "pages": pages, "page_num": page_num,
                     "less_than_certain_size": less_than_certain_size}

        self.render("www/w_staff_goods.html",
                    category_list=category_list, goods_list=goods_list,
                    count=goods_count, page_args=page_args, num=num)


urls = [
    (r"/staff_goods/?", WwwwStaffGoodsHandler),
]
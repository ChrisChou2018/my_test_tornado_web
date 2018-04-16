#!/usr/bin/env python
# coding:utf-8

import urllib
from time import mktime, time

from meihuishuo.libs.handlers import WwwBaseHandler
from meihuishuo.models.goods_model import Goods, HomeLimitedGoods, Country, \
    Collection
# from meihuishuo.models import goods_model
from meihuishuo.models.home_model import Shop
from meihuishuo.models.shop_model import Type
from meihuishuo.libs.pagination import Paginator


class WwwGoodsSearchBase(WwwBaseHandler):

    def get_goods_info(self, limit_goods, goods_list):
        """获取产品信息
        """

        limited_goods_list = []
        for goods in goods_list:
            goods_info = {}

            if self.current_user:
                member_id = self.current_user.member_id
                collection_count = Collection.get_colletion_id_count(member_id, goods.goods_id)
                if collection_count:
                    goods_info["is_favorite"] = "1"
                else:
                    goods_info["is_favorite"] = "0"
            else:
                goods_info["is_favorite"] = "0"
            goods_info["price"] = str(goods.current_price)
            goods_info["goods_intro"] = goods.goods_intro
            goods_info["buy_count"] = goods.buy_count
            goods_info["goods_brief_intro"] = goods.abbreviation
            goods_info["domestic_price"] = goods.domestic_price
            goods_info["id"] = goods.goods_id
            goods_info["img_url"] = self.build_photo_url(goods.img_view, pic_version="smdl", pic_type="goods", cdn=True)
            goods_info["title"] = goods.goods_title
            goods_info["country"] = ""
            goods_info["country_img_url"] = ""
            goods_info["brand"] = ""
            goods_info["limited_end_at"] = None
            goods_info["stock_count"] = int(goods.stock)
            if goods_info["stock_count"] < 1:
                goods_info["is_sold_out"] = 1
            else:
                goods_info["is_sold_out"] = 0

            limited_goods_list.append(goods_info)

        return limited_goods_list


class WwwGoodsSearch(WwwGoodsSearchBase):
    def get(self):
        category_list = self.get_category()

        search_data = {}
        search_data["search"] = urllib.unquote(self.get_argument("key", None))
        result = []
        category_name = search_data["search"]
        if not search_data["search"]:
            # "抱歉，没有找到与“”相关的商品"
            self._render()

        # 排序字段: 热卖：host(default)；价格：price；新品：time；好评：score
        search_data["order_name"] = self.get_argument("order_name", "hot")
        sort = self.get_argument("sort", "")
        if sort == "1":
            search_data["order_type"] = "asc"
        else:
            search_data["order_type"] = "desc"
        page_num = self.get_argument("page_num", "1")
        search_data["page_num"] = int(page_num) if page_num.isdigit() and \
            int(page_num) > 0 else 1
        gs_list = Goods.search_goods(search_data,
                                     num_per_page=60,
                                     version="new")
        count = Goods.search_goods(search_data,
                                   version="new",
                                   is_count=True)
        goods_ids = [each.goods_id for each in gs_list]
        if goods_ids:
            limited_goods = HomeLimitedGoods.list_all_goods(goods_ids)
            result = self.get_goods_info(limited_goods, gs_list)
            goods_list = result if result else []
        else:
            goods_list = []

        paginator = Paginator(count, 60)
        page = paginator.page(search_data["page_num"])
        pages = paginator.calculate_display_pages(search_data["page_num"])
        page_num = paginator.total_pages
        less_than_certain_size = paginator.check_less_than_certain_size()
        page_args = {"page": page, "pages": pages,
                     "less_than_certain_size": less_than_certain_size,
                     "current_page": search_data["page_num"],
                     "page_num": page_num}
        self._render(category_list, goods_list, count, sort,
                     category_name, search_data["order_name"],
                     page_args,search_data["search"])

    def _render(self, category_list=[], goods_list=[], count=0,
                sort="1", category_name="", sort_name="hot",
                page_args=None, key="", statu_code=200):
        # if statu_code != 200:
        #     if statu_code == 404:
        #         self.send_error(404)
        #     self.render("www/{0}.html".format(statu_code))

        self.render("www/w_search.html",
                    category_list=category_list, goods_list=goods_list,
                    count=count, parent=None, parent_name=None,
                    category_name=category_name, sort_name=sort_name,
                    page_args=page_args, sort=sort, search_key=key)


class WwwGoodsCategory(WwwGoodsSearchBase):
    def get(self):
        category_list = self.get_category()
        category_id = self.get_argument("id", None)
        parent = self.get_argument("parent", "").strip("null")
        if not category_id:
            self._render(category_list, [], "0")

        parent_name = ""
        if parent:
            parent_type = Type.load_type_by_uuid(parent)
            if parent_type:
                parent_name = parent_type.title
        category_type = Type.load_type_by_uuid(category_id)
        category_name = ""
        if category_type:
            category_name = category_type.title

        search_data = {}
        page_num = self.get_argument("page_num", "1")
        search_data["page_num"] = int(page_num) if page_num.isdigit() and \
            int(page_num) > 0 else 1
        search_data["type"] = "categories"
        sort = self.get_argument("sort", "")
        if sort == "1":
            search_data["sort_type"] = "asc"
        else:
            search_data["sort_type"] = "desc"
        search_data["sort_name"] = self.get_argument("order_name", "hot")

        type_list = Type.list_sub_type(category_id)

        type_ids = [each.uuid for each in type_list]
        type_ids.append(category_id)
        search_data["ids"] = type_ids

        gs_list, count = Goods.list_categories_goods(search_data)
        if gs_list:
            goods_ids = [each.goods_id for each in gs_list]
            if goods_ids:
                limited_goods = HomeLimitedGoods.list_all_goods(goods_ids)
                result = self.get_goods_info(limited_goods, gs_list)
                goods_list = result if result else []
            else:
                goods_list = []
        else:
            goods_list = []

        paginator = Paginator(count, 60)
        page = paginator.page(search_data["page_num"])
        pages = paginator.calculate_display_pages(search_data["page_num"])
        page_num = paginator.total_pages
        less_than_certain_size = paginator.check_less_than_certain_size()
        page_args = {"page": page, "pages": pages,
                     "less_than_certain_size": less_than_certain_size,
                     "current_page": search_data["page_num"],
                     "page_num": page_num}

        self._render(category_list, goods_list, sort, count,
                     parent, parent_name, category_name,
                     search_data["sort_name"], page_args)

    def _render(self, category_list=[], goods_list=[], sort="1",
                count=0, parent=None, parent_name="",
                category_name="", sort_name="hot",
                page_args=None, statu_code=200):
        # if statu_code != 200:
        #     if statu_code == 404:
        #         self.send_error(404)
        #     self.render("www/{0}.html".format(statu_code))

        self.render("www/w_search.html",
                    category_list=category_list, goods_list=goods_list,
                    count=count, parent=parent, parent_name=parent_name,
                    category_name=category_name, sort_name=sort_name,
                    page_args=page_args, sort=sort, search_key="")


urls = [
    (r"/search/?", WwwGoodsSearch),
    (r"/category/?", WwwGoodsCategory),
]

#!/usr/bin/env python
# coding:utf-8

from datetime import datetime, timedelta
from time import mktime, time
import json
import urllib

from meihuishuo.libs.handlers import WwwBaseHandler, JsWwwBaseHandler
from meihuishuo.libs.decorators import www_authenticated
from meihuishuo.models.shop_model import Type
from meihuishuo.models import shop_cart_model
from meihuishuo.models.shop_cart_model import ShopCart
from meihuishuo.models.goods_model import HomeLimitedGoods, Goods, Country, StaffGoods
from meihuishuo.models.home_model import Shop

# Type parent id


class WwwCartHandler(WwwBaseHandler):
    def get(self):
        category_list = self.get_category()

        if not self.current_user:
            try:
                mhs_cart = urllib.unquote(self.get_cookie("mhs-cart"))
            except Exception as e:
                mhs_cart = None
            result = []
            if mhs_cart:
                cart = json.loads(mhs_cart)

                ids = []
                count_map = {}
                for goods in cart['items']:
                    ids.append(goods["GoodsId"])
                    count_map[goods["GoodsId"]] = goods['Count']
                if ids:
                    result = self.getTmpCartData(ids, count_map)

        else:
            member_id = self.current_user.member_id
            result = shop_cart_model.app_cart_goods_list(member_id, version="new",
                                                         status="all_goods")
            if result:
                goods_ids = [each["goods_id"] for each in result]
                limited_goods = HomeLimitedGoods.list_limited_goods_by_goods_ids(goods_ids)
                staff_goods = StaffGoods.list_goods_by_ids(goods_ids, online=True)
                goods_list = Goods.list_goods_by_ids(goods_ids, status="all_goods")

                g_ids = list()
                for goods in goods_list:
                    g_ids.append(goods.goods_id)
                    # if not goods.stock.isdigit():
                    #     goods.stock = 0
                    goods.stock = int(goods.stock)
                    for each in limited_goods:
                        if each.goods_id == goods.goods_id:
                            if each.goods_limited_price < goods.price:
                                goods.price = each.goods_limited_price
                            if each.goods_left_count < goods.stock:
                                goods.stock = each.goods_left_count
                            break

                for each in result:
                    each["is_not_avail"] = 0
                    each["is_sold_out"] = 0
                    for goods in goods_list:
                        each["staff_goods"] = False
                        for item in staff_goods:
                            if item.goods_id == each["goods_id"]:
                                each["price"] = item.price
                                if item.stock < goods.stock:
                                    goods.stock = item.stock
                                goods.status = item.status
                                goods.sale_type = None
                                each["staff_goods"] = True
                                break

                        if goods.goods_id == each["goods_id"]:
                            if int(each["goods_count"]) > goods.stock:
                                each["is_sold_out"] = 1
                            each["stock"] = goods.stock
                            each["new_buyer"] = True if goods.sale_type == "new_buyer" else False
                            if goods.status != "1":
                                each["is_not_avail"] = 1
                            break
                    each["goods_img_url"] = self.build_photo_url(each["goods_img_url"], pic_type="goods", cdn=True)
                    if each["country_img_url"]:
                        each["country_img_url"] = self.build_country_img_url(each["country_img_url"])
                    else:
                        each["country_img_url"] = ""

        self.render("www/w_cart.html",
                    category_list=category_list, cart_goods=(result or []))

    def getTmpCartData(self, ids, count_map):
        #
        # 生成临时的购物车列表(未登录时生成的购物车列表)
        #
        goods_list = Goods.find_order_goods_list(ids)
        result = []
        limited_goods = HomeLimitedGoods.list_limited_goods_by_goods_ids(ids)
        for goods in goods_list:
            # 获取最低价格和最小库存
            cart_goods_dict = {}
            goods.stock = int(goods.stock)
            for each in limited_goods:
                if each.goods_id == goods.goods_id:
                    if each.goods_limited_price < float(goods.price):
                        goods.price = str(each.goods_limited_price)
                    if each.goods_left_count < goods.stock:
                        goods.stock = each.goods_left_count
                    # if each.goods_left_count < goods["goods_count"]:
                    #     cart_goods_dict["goods_count"] = l_goods.goods_left_count
                    break

            if goods.shop_id:
                country_id = Shop.get_country_id_by_shop_id(goods.shop_id)
                country = Country.get_country(country_id)
                cart_goods_dict["country_img_url"] = country.country_id
            else:
                cart_goods_dict["country_img_url"] = None

            cart_goods_dict["cart_item_id"] = goods.goods_id
            cart_goods_dict["goods_id"] = goods.goods_id
            cart_goods_dict["goods_img_url"] = self.build_photo_url(goods.img_view, pic_type="goods", cdn=True)
            cart_goods_dict["domestic_price"] = goods.domestic_price
            cart_goods_dict["price"] = str(goods.current_price)
            cart_goods_dict["goods_title"] = goods.goods_title
            cart_goods_dict["weight"] = goods.weight
            cart_goods_dict["goods_brief_intro"] = goods.abbreviation
            cart_goods_dict["stock"] = goods.stock
            cart_goods_dict["goods_count"] = count_map[goods.goods_id]

            cart_goods_dict["is_not_avail"] = 0
            cart_goods_dict["is_sold_out"] = 0
            cart_goods_dict["new_buyer"] = True if goods.sale_type == "new_buyer" else False
            if goods.status != "1":
                cart_goods_dict["is_not_avail"] = 1
            if int(cart_goods_dict["goods_count"]) > goods.stock:
                cart_goods_dict["is_sold_out"] = 1

            result.append(cart_goods_dict)

        return result


class WwwCartDeleteHandler(WwwBaseHandler):
    @www_authenticated
    def post(self):
        cart_goods = self.get_argument("id", None)
        cart_goods_list = self.get_argument("ids", None)
        if not cart_goods and not cart_goods_list:
                self.data["status"] = "error"
                self.data["message"] = "删除购物车商品失败"
                self.write(self.data)
                return

        # cart_ids = json.loads(cart_goods)
        if cart_goods:
            ids = [cart_goods]

        if cart_goods_list:
            ids = cart_goods_list.split("#")

        try:
            ShopCart.delete_cart_batch(ids)
        except:
            self.data["status"] = "error"
            self.data["message"] = "删除购物车商品失败"
            self.write(self.data)
            return

        self.data["status"] = "success"
        self.write(self.data)


class WwwCartAddHandler(WwwBaseHandler):
    @www_authenticated
    def post(self):
        goods_id = self.get_argument("id", None)
        count = self.get_argument("count", None)

        if not goods_id:
            self.data["message"] = "商品为空"
            self.write(self.data)
            return

        current_user = self.current_user
        if current_user and current_user.is_staff:
            goods = Goods.get_goods_by_goods_id(goods_id, goods_status="all_status")
        else:
            goods = Goods.get_goods_by_goods_id(goods_id, api="insert")
        limited_goods = HomeLimitedGoods.load_limited_goods_by_goods_id(goods_id)
        if not goods:
            self.data["status"] = "error"
            self.data["message"] = "商品已经下架"
            self.write(self.data)
            return

        member_id = self.current_user.member_id
        force_insert = False
        cart_goods = shop_cart_model.ShopCart.load_shop_cart_goods(member_id, goods_id)
        if not cart_goods:
            force_insert = True
            cart_goods = shop_cart_model.ShopCart()
            cart_goods.goods_id = goods_id
            cart_goods.member_id = self.current_user.member_id
            cart_goods.create_time = datetime.now()

        if limited_goods:
            # if not goods.stock.isdigit():
            #     goods.stock = 0
            if limited_goods.goods_left_count < int(goods.stock):
                goods.stock = limited_goods.goods_left_count
            else:
                goods.stock = int(goods.stock)

        current_user = self.current_user
        is_staff_goods = False
        if current_user.is_staff:
            staff_goods = StaffGoods.load_goods_by_id(goods_id, online=True)
            if staff_goods:  # 不是内购商品
                is_staff_goods = True
                goods.stock = staff_goods.stock

        if int(cart_goods.goods_count) >= goods.stock:
            self.data["status"] = "error"
            self.data["message"] = "商品库存不足"
            self.write(self.data)
            return

        if (int(cart_goods.goods_count) + int(count)) > 99:
            self.data["status"] = "error"
            self.data["message"] = "单件商品的数量不能超过99件"
            self.write(self.data)
            return

        change_count = int(count) if count else 0
        if is_staff_goods:
            cart_goods.goods_count = str(int(cart_goods.goods_count)  + int(count))
            change_count = int(count)
        else:
            if goods.sale_type == "new_buyer":
                if cart_goods.goods_count == "0":
                    change_count = 1
                else:
                    change_count = 1-int(cart_goods.goods_count)
                cart_goods.goods_count = "1"
            else:
                cart_goods.goods_count = str(int(cart_goods.goods_count)  + int(count))
                change_count = int(count)

        cart_goods.save(force_insert=force_insert)

        self.data["status"] = "success"
        self.data["change_count"] = change_count
        self.write(self.data)


class WwwCartUpdateHandler(WwwBaseHandler):
    @www_authenticated
    def post(self):
        goods_id = self.get_argument("goods_id", None)
        goods_count = self.get_argument("goods_count", None)

        member_id = self.current_user.member_id

        if goods_id and goods_count:
            item = ShopCart.load_shop_cart_goods(member_id, goods_id)

            if not item:
                self.data["status"] = "error"
                self.data["message"] = "商品不存在"
                self.write(self.data)
                return

            cart_goods = Goods.get_goods_by_goods_id(goods_id, goods_status="all_goods")
            limited_goods = HomeLimitedGoods.load_limited_goods_by_goods_id(cart_goods.goods_id)
            staff_goods = StaffGoods.load_goods_by_id(cart_goods.goods_id, online=True)

            if not cart_goods.stock:
                cart_goods.stock = 0
            if staff_goods:
                if int(cart_goods.stock) > staff_goods.stock:
                    cart_goods.stock = staff_goods.stock
                else:
                    cart_goods.stock = cart_goods.stock
            elif limited_goods:
                if int(cart_goods.stock) > limited_goods.goods_left_count:
                    cart_goods.stock = limited_goods.goods_left_count
                else:
                    cart_goods.stock = cart_goods.stock

            if int(goods_count) > 99:
                self.data["status"] = "error"
                self.data["message"] = "单件商品购买的数量不能超过99件"
                self.write(self.data)
                return

            if int(goods_count) > int(cart_goods.stock):
                self.data["status"] = "error"
                self.data["message"] = "商品库存不足"
                self.write(self.data)
                return

            try:
                ShopCart.update_cart(item.uuid, int(goods_count))
                self.data["status"] = "success"
            except:
                self.data["status"] = "error"
                self.data["message"] = "购物车更新失败"
                self.write(self.data)
                return

        self.write(self.data)


class WwwCartCounteHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        """获取购物车数量
        """

        member_id = self.current_user.member_id
        count = ShopCart.get_cart_count(member_id)

        self.data["status"] = "success"
        self.data["count"] = count
        self.write(self.data)

urls = [
    (r"/cart/?", WwwCartHandler),
    (r"/cart/delete/?", WwwCartDeleteHandler),
    (r"/cart/add/?", WwwCartAddHandler),
    (r"/cart/update/?", WwwCartUpdateHandler),
    (r"/cart/count/?", WwwCartCounteHandler),
]

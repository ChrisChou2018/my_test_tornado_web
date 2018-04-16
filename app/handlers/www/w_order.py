#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter

from meihuishuo.libs.handlers import WwwBaseHandler, JsWwwBaseHandler
from meihuishuo.libs.decorators import www_authenticated
from meihuishuo.models.order_model import Order, OrderGoods, PayLog, \
    delete_order_goods, Logistics
from meihuishuo.models.goods_model import Goods, Comment, StaffGoods
from meihuishuo.models.coupon_model import Coupon


class WJsCancelOrderHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        order_id = self.get_argument("order_id", None)
        group_buy_order = self.get_argument("group_buy_order", None)
        member_id = self.current_user.member_id

        if order_id and member_id:
            order = Order.load_order_by_order_and_member_id(order_id, member_id)
            if not order:
                self.data["message"] = "订单不存在"
                self.write(self.data)
                return

            if order.coupon_id:
                Coupon.update_coupon(order.coupon_id, {"is_used":0})

            if delete_order_goods(order_id, member_id) == 0:
                self.data["message"] = "订单不存在"
            else:
                self.data["result"] = "success"
        else:
            self.data["message"] = "订单不存在"

        self.write(self.data)


class WMyOrderHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        status = self.get_argument("status", "0")
        order_id = self.get_argument("order_id", None)

        category_list = self.get_category()

        order_list = []
        member_id = self.current_user.member_id
        my_order_list = Order.get_my_order(member_id, "0")
        if order_id:
            status = "0"
            order = Order.load_my_order_by_id(member_id, order_id)
            order_list = [order] if order else []
        else:
            order_list = Order.get_my_order(member_id, status)

        status_counter = Counter()
        status_counter.update([order.status for order in my_order_list])

        wait_review_order_ids = [order.order_id
                                 for order in Order.get_my_order(member_id, "4")
                                 ]
        order_goods = OrderGoods.list_order_goods_by_order_ids(wait_review_order_ids)
        order_goods_ids = [each.goods_id for each in order_goods]
        hava_comment_goods_ids = [each.goods_id
                                  for each in Comment.list_comment(order_goods_ids, member_id)
                                  ]
        wait_review_order_list = []
        for goods in order_goods:
            if goods.goods_id not in hava_comment_goods_ids:
                if goods.order_id not in wait_review_order_list:
                    wait_review_order_list.append(goods.order_id)
                    status_counter.update("9")

        ordergoods_list = comment_list = []
        goods_list = []
        if order_list:
            order_id_list = [each.order_id for each in order_list]
            ordergoods_list = OrderGoods.list_order_goods_by_order_ids(order_id_list)
            if ordergoods_list:
                goods_id_list = [each.goods_id for each in ordergoods_list]
                goods_list = Goods.find_order_goods_list(goods_id_list)
                comment_list = Comment.list_comment(goods_id_list, member_id)

                if self.current_user.is_staff:
                    staff_goods_list = StaffGoods.list_goods_by_ids(goods_id_list, online=True)
                    for goods in goods_list:
                        for item in staff_goods_list:
                            if goods.goods_id == item.goods_id:
                                goods.current_price = item.price

        result_order_list = []
        for order in order_list:
            result_order = {}
            result_order["id"] = order.order_id
            result_order["goods"] = []
            is_comment = False
            for order_goods in ordergoods_list:
                # 查找是否是等待评价
                for comment in comment_list:
                    if comment.goods_id == order_goods.goods_id:
                        is_comment = True
                        break
                if is_comment and status == "4":
                    break

                if order.order_id == order_goods.order_id:
                    for goods in goods_list:
                        order_info = {}
                        if goods.goods_id == order_goods.goods_id:
                            order_info["order_id"] = order.order_id
                            if goods.img_view:
                                if "http" not in goods.img_view:
                                    order_info["goods_img_url"] = self.build_photo_url(goods.img_view, pic_type="goods", cdn=True)
                                else:
                                    order_info["goods_img_url"] = goods.img_view
                            else:
                                order_info["goods_img_url"] = ""
                            order_info["count"] = order_goods.goods_count
                            order_info["goods_title"] = goods.goods_title
                            order_info["goods_id"] = goods.goods_id
                            if order.status in ["11", "12", "13", "14", "15", "16"]:
                                order_info["price"] = str(goods.groupbuy_price)
                            else:
                                order_info["price"] = str(goods.current_price)
                            result_order["goods"].append(order_info)

            if status == 4 and is_comment:
                break

            if result_order["goods"]:
                result_order["totle_price"] = order.price
                result_order["order_status"] = order.status
                result_order["is_group_order"] = False
                if order.status in ["11", "12", "13", "14", "15", "16"]:
                    result_order["is_group_order"] = True
                result_order["create_time"] = order.create_time
                result_order_list.append(result_order)

        self.render("www/w_my_order.html",
                    order_list=result_order_list, status_counter=status_counter,
                    status=status, order_id=order_id, my_order_list=my_order_list,
                    category_list=category_list)


class WOrderDetailHandler(WwwBaseHandler):
    @www_authenticated
    def get(self, order_id):
        category_list = self.get_category()

        order = goods_list = None
        if not order_id:
            self.render("m_mobile/m_order_detail.html",
                        order=order, goods_list=goods_list)

        current_user = self.current_user
        member_id = current_user.member_id
        order = Order.load_order_by_order_and_member_id(order_id, member_id)
        goods = activitys = coupon = None
        if not order:
            self.render("www/w_order_detail.html",
                        category_list=category_list, order=order)
            return

        goods_list = OrderGoods.get_order_goods_by_order_id(order.order_id)
        if not goods_list:
            self.render("www/w_order_detail.html",
                        category_list=category_list, goods_list=goods_list)
            return

        goods_id_list = []
        activity_id_list = []
        for each in goods_list:
            goods_id_list.append(each.goods_id)
            activity_id_list.append(each.activity_id)
        if goods_id_list:
            goods = Goods.find_order_goods_list(goods_id_list)
            if current_user.is_staff:
                staff_goods_list = StaffGoods.list_goods_by_ids(goods_id_list, online=True)
                for item in goods:  # 限时商品限时价格
                    for staff_goods in staff_goods_list:
                        if item.goods_id == staff_goods.goods_id:
                            item.current_price = staff_goods.price

        # 商品总价格
        total_price = 0
        for item in goods_list:
            for each in goods:
                if item.goods_id == each.goods_id:
                    if order.status in ["11", "12", "13", "14", "15", "16"]:
                        price = each.groupbuy_price
                    else:
                        price = each.current_price
                    total_price += price * int(item.goods_count)

        if order.coupon_id:
            coupon = Coupon.load_coupon_by_coupon_id(order.coupon_id)

        self.render("www/w_order_detail.html",
                    category_list=category_list, order=order,
                    goods_list=goods_list, goods=goods,
                    coupon=coupon, total_price=total_price)


class WwwLogisticsHandler(JsWwwBaseHandler):
    @www_authenticated
    def get(self):

        order_id = self.get_argument("order_id", None)

        if not order_id:
            self.data["result"] = "error"
            self.data["message"] = "订单号有误"
            self.write(self.data)
            return

        logistic_list = Logistics.list_logistics_by_order_ids([order_id])
        logistics = []
        order = Order.load_order_by_id(order_id)
        if not order:
            order_time = ""
        else:
            if order.pay_time:
                order_time = order.pay_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                order_time = ""

        if not logistic_list:
            self.data["company_name"] = ""
            self.data["waybill"] = ""
            logistics.append({"content":"订单已支付，正在配货中...",
                              "handling_time":order_time})
            self.data["logistics"] = logistics
            self.data["result"] = "success"
            self.write(self.data)
            return

        self.data["company_name"] = logistic_list[len(logistic_list)-1].logistics_name
        self.data["waybill"] = logistic_list[len(logistic_list)-1].way_num

        for each in logistic_list:
            logistic_dict = {}
            logistic_dict["content"] = each.content
            logistic_dict["handling_time"] = each.handling_time.strftime("%Y-%m-%d %H:%M:%S")
            logistics.append(logistic_dict)

        self.data["logistics"] = logistics
        self.data["result"] = "success"
        self.write(self.data)


class LogisticsHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        status = self.get_argument("status", "0")
        order_id = self.get_argument("order_id", None)

        category_list = self.get_category()

        member_id = self.current_user.member_id
        member_name = self.current_user.member_name
        my_order_list = Order.get_my_order(member_id, "0")

        status_counter = Counter()
        status_counter.update([order.status for order in my_order_list])

        wait_review_order_ids = [order.order_id
                                 for order in Order.get_my_order(member_id, "4")
                                 ]
        order_goods = OrderGoods.list_order_goods_by_order_ids(wait_review_order_ids)
        order_goods_ids = [each.goods_id for each in order_goods]
        hava_comment_goods_ids = [each.goods_id
                                  for each in Comment.list_comment(order_goods_ids, member_id)
                                  ]
        wait_review_order_list = []
        for goods in order_goods:
            if goods.goods_id not in hava_comment_goods_ids:
                if goods.order_id not in wait_review_order_list:
                    wait_review_order_list.append(goods.order_id)
                    status_counter.update("9")

        logistic_list = Logistics.list_logistics_by_order_ids([order_id])
        logistics = []
        order = Order.load_order_by_id(order_id)
        if not order:
            order_time = ""
        else:
            if order.pay_time:
                order_time = order.pay_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                order_time = ""

        if not logistic_list:
            self.data["company_name"] = ""
            self.data["waybill"] = ""
            logistics.append({"content":"订单已支付，正在配货中...",
                              "handling_time":order_time})
            company_name = "无"
            waybill = "无"
        else:
            company_name = logistic_list[len(logistic_list)-1].logistics_name
            waybill = logistic_list[len(logistic_list)-1].way_num

        for each in logistic_list:
            logistic_dict = {}
            logistic_dict["content"] = each.content
            logistic_dict["handling_time"] = each.handling_time.strftime("%Y-%m-%d %H:%M:%S")
            logistics.append(logistic_dict)

        self.render("www/w_logistics.html",
                    status_counter=status_counter, status=status,
                    order=order, category_list=category_list,
                    company_name=company_name, waybill=waybill,
                    logistics=logistics, member_name=member_name)


class WwwFinishOrderHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        order_id = self.get_argument("order_id", None)
        groupbuy = self.get_argument("groupbuy", None)
        member_id = self.current_user.member_id

        if order_id and member_id:
            if groupbuy == "Y":
                status = "group_buy_order"
            else:
                status = "common_order"
            if Order.finish_order(order_id, member_id, status)==0:
                self.data["message"] = "订单不存在"
            else:
                self.data["result"] = "success"
        else:
            self.data["message"] = "数据异常，请刷新重试"
        self.write(self.data)


urls = [
    (r"/my_order/?", WMyOrderHandler),
    (r"/my_order/delete/?", WJsCancelOrderHandler),
    (r"/my_order/([a-z0-9-]+)/?", WOrderDetailHandler),
    (r"/order/logistics/?", WwwLogisticsHandler),
    (r"/logistics/?", LogisticsHandler),
    (r"/order/finish/?", WwwFinishOrderHandler),
]

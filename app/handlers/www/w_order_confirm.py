#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import uuid
from datetime import datetime, timedelta
import random
from urllib import urlencode
from hashlib import md5
import base64
try:
    import cStringIO as StringIO
except:
    import StringIO

import urllib2
import qrcode
import meihuishuo.libs.common as lib_common

from meihuishuo.libs.handlers import WwwBaseHandler, JsWwwBaseHandler
from meihuishuo.libs.decorators import www_authenticated
from meihuishuo.models.member_model import Address
from meihuishuo.models import order_model
from meihuishuo.models.order_model import Order, OrderGoods, OrderStatus, PayLog, \
    params_filter
from meihuishuo.models.shop_cart_model import ShopCart
from meihuishuo.models import goods_model
from meihuishuo.models.goods_model import Goods, HomeLimitedGoods
from meihuishuo.models.coupon_model import Coupon
from meihuishuo.libs.order import check_order_is_new_buyer_order


class WwwOrderConfirmHandler(WwwBaseHandler):
    @www_authenticated
    def post(self):

        current_user = self.current_user
        member_id = current_user.member_id
        from_data = self.get_argument("from", None)
        address_id = self.get_argument("address", None)
        goods_list = self.get_arguments("goods")

        self.order = {}

        goods_map = {}
        goods_ids = []
        for goods in goods_list:
            goods_info = goods.split(":")
            if len(goods_info) == 2:
                goods_map[goods_info[0]] = goods_info[1]
                goods_ids.append(goods_info[0])

        while True:
            now_time = time.strftime('%Y%m%d%H', time.localtime(time.time()))
            self.order["uuid"] = now_time + str(random.random())[3:7]
            if not Order.order_exists_or_not(self.order["uuid"]):
                break

        self.order["member_id"] = member_id
        self.order["login_type"] = "pc"
        self.order["deliver_type"] = "3"
        self.order["create_person"] = member_id
        self.order["update_person"] = member_id
        self.order["create_time"] = datetime.now()
        self.order["update_time"] = datetime.now()

        address = Address.find_by_id(address_id)
        self.order["collect_area"] = address.area
        self.order["collect_address"] = address.area + " " + address.address
        self.order["collect_person"] = address.addressee
        self.order["collect_tel"] = address.telephone
        self.order["activity_id"] = str(uuid.uuid4())

        # self.order["Status"] = "1"
        self.order["is_finish"] = "0"
        self.order["deliver_cost"] = "0"
        self.order["distribution"] = 1  # 支付方式：distribution【1：支付宝，2：微信支付】

        if self.order["deliver_type"] == "1":
            self.order["deliver_type"] = u"工作日送货"
        elif self.order["deliver_type"] == "2":
            self.order["deliver_type"] = u"节假日送货"
        elif self.order["deliver_type"] == "3":
            self.order["deliver_type"] = u"均可配送"

        is_staff_order = self.get_argument("staff_order", None)
        if is_staff_order == "1" or is_staff_order == '0':
            staff_order = True
            if is_staff_order == "1":
                self.order["unified_order"] = True
            else:
                self.order["unified_order"] = False
        else:
            staff_order = False
            self.order["unified_order"] = False
        self.order["staff_order"] = staff_order

        goods_list = goods_model.list_goods_min_price(goods_ids, status="all_goods")
        self.order["price"] = 0
        goods_list_ids = [each.goods_id for each in goods_list]

        # 是否存在内购商品
        staff_goods_list = goods_model.StaffGoods.list_goods_by_ids(goods_ids, online=True)
        # 有普通和内购商品
        is_staff = False
        if staff_goods_list:
            if len(staff_goods_list) != len(goods_list):
                self.data["message"] = "不能同时购买内购商品和普通商品"
                self.write(self.data)
            else:
                if current_user.is_staff:
                    is_staff = True

        # 对应的商品生成的对应： 订单-商品 关系
        goods_count = 0
        new_buyer_count = 0
        goods_add = []
        for goods in goods_list:
            for goods_id, count in goods_map.items():
                if goods_id == goods.goods_id:
                    goods_i = {}

                    if current_user.is_staff:
                        for item in staff_goods_list:
                            if goods.goods_id == item.goods_id:
                                goods.current_price = item.price
                                break

                    goods_i["uuid"] = str(uuid.uuid4())  # OrderGoods.uuid
                    goods_i["order_id"] = self.order["uuid"]  # OrderGoods.order_id
                    goods_i["goods_id"] = goods_id  # OrderGoods.goods_id
                    goods_i["goods_count"] = int(count)  # OrderGoods.goods_count
                    goods_i["price"] = goods.current_price  # OrderGoods.goods_id
                    goods_i["title"] = goods.goods_title
                    goods_add.append(goods_i)
                    goods_count += int(count)
                    if goods.sale_type == "new_buyer":
                        new_buyer_count += int(count)
                    break

        # 不是内购商品时候, 判断是否是享有新人商品
        if not staff_goods_list and new_buyer_count >= 1:
            is_newbuyer = True
            orders = [o for o in Order.get_order_by_member_id(member_id)]
            if orders:
                for each in orders:
                    if each.status in ["2", "3", "4"]:
                        is_newbuyer  =False
            elif new_buyer_count > 1:
                is_newbuyer  =False

            if not is_newbuyer:
                self.redirect("/cart")
                return

        # 存在不可用的商品
        unavail = False
        for goods_id in goods_ids:
            if goods_id not in goods_list_ids:
                unavail = True
                break

        # 判断商品库存，并生成价格
        soldout = False
        for goods in goods_list:
            goods.stock = int(goods.stock)
            # for each in self.order["goods_list"]:
            for goods_id, count in goods_map.items():
                if goods_id == goods.goods_id:
                    if goods.stock < int(count):
                        soldout = True
                    else:
                        self.order["price"] += goods.current_price * int(count)

        # 直接下单加 6 元邮费
        if is_staff_order == '0':
            self.order["price"] += 6

        if unavail or soldout:
            self.data["status"] = "error"
            return

        # 添加优惠券信息
        coupon_id = self.get_argument("order_coupon", None)
        if coupon_id:
            coupons = Coupon.list_coupons_by_status(status="unused",
                                                    owner_id=member_id,
                                                    now_time=int(time.time()),
                                                    api_use="create_order")
            if coupons:
                for each in coupons:
                    if each.coupon_id == int(coupon_id):
                        self.order["coupon_id"] = coupon_id
                        self.order["price"] = str(float(self.order["price"])-
                                                  each.face_value)
                        self.order["coupon_id"] = coupon_id
                        each.is_used = 1
                        each.save()
                        break

        delete_map = {}
        delete_map["member_id"] = member_id
        goods_del_list = []
        for goods_id in goods_ids:
            goods_del_list.append({"goods_id": goods_id})
        delete_map["goods_info"] = goods_del_list
        if not self.order["price"] or float(self.order["price"]) <= 0:
            self.order["price"] = "0"
        if float(self.order["price"]) == 0:
            self.data["no_payment_needed"] = "Y"
            for goods_id, count in goods_map.items():
                Goods.update_goods_stock(goods_id, int(count))
                HomeLimitedGoods.update_goods_stock(goods_id, int(count))

        self.order["status"] = "1"
        if float(self.order["price"]) == 0:
            self.order["status"] = "2"
        if from_data == "cart":
            # 删除相应的购物车
            ShopCart.delete_shop_cart_goods_batch(delete_map, "new")
        Order.add(self.order, "new")
        OrderGoods.add_list(goods_add, "new")
        OrderStatus.add_order_status(self.order)

        self.redirect("/order/pay?order_id="+self.order["uuid"])

    @www_authenticated
    def get(self):
        sum_price = 0  # 存储应付总金额
        category_list = self.get_category()

        current_user = self.current_user
        member_id = current_user.member_id
        address = Address.find_all(member_id)
        address_list = []
        default_address = None
        for each in address:
            default_address_id = current_user.default_address_id
            if default_address_id == each.address_id:
                default_address = {}
                default_address["address_id"] = each.address_id
                default_address["collect_address"] = each.address
                default_address["collect_person"] = each.addressee
                default_address["telephone"] = each.telephone
                default_address["area"] = each.area
            else:
                each_dict = dict()
                each_dict["address_id"] = each.address_id
                each_dict["collect_address"] = each.address
                each_dict["collect_person"] = each.addressee
                each_dict["telephone"] = each.telephone
                each_dict["area"] = each.area
                address_list.append(each_dict)

        new_buyer_count = 0  # 新有优惠商品总数量
        is_newbuyer = True  # 是否是享有该新人优惠商品
        mix_staff_and_goods = False  # 是否包含内购商品和别的
        staff_goods_list = []
        count = self.get_argument("count", None)
        if count is None:
            goods_l = self.get_arguments("goods")
            goods_list_info = {}
            goods_ids = []
            for goods in goods_l:
                if goods:
                    goods_id, count = goods.split(":")
                    goods_list_info[goods_id] = int(count)
                    goods_ids.append(goods_id)

            goods_list = goods_model.list_goods_min_price(goods_ids, status="all_goods")
            # 是否存在内购商品
            if current_user.is_staff:
                staff_goods_list = goods_model.StaffGoods.list_goods_by_ids(goods_ids, online=True)
                # 有普通和内购商品
                if staff_goods_list and len(staff_goods_list) != len(goods_list):
                    mix_staff_and_goods = True

            # 获取只需要的商品信息
            result = []  # 存放结果
            for goods in goods_list:
                for goods_id, count in goods_list_info.items():
                    goods_info = {}

                    if current_user.is_staff:
                        for item in staff_goods_list:
                            if goods.goods_id == item.goods_id:
                                goods.current_price = item.price
                                break

                    if goods_id == goods.goods_id:
                        if goods.sale_type == "new_buyer":
                            new_buyer_count += int(count)
                        goods_info["id"] = goods_id
                        goods_info["count"] = count
                        goods_info["price"] = str(goods.current_price)
                        goods_info["img"] = self.build_photo_url(goods.img_view, pic_type="goods", cdn=True)
                        goods_info["title"] = goods.goods_title
                        goods_info["total_price"] = goods.current_price * int(count)
                        result.append(goods_info)
                        sum_price += goods_info["total_price"]
                        break

        else:
            goods_id = self.get_argument("goods_id", None)
            goods_ids = []
            if not goods_id or not count:
                result = []
            else:
                goods_ids.append(goods_id)
                goods_list = goods_model.list_goods_min_price(goods_ids, status="all_goods")

                if current_user.is_staff:
                    # 是否存在内购商品
                    staff_goods_list = goods_model.StaffGoods.list_goods_by_ids(goods_ids, online=True)
                    # 有普通和内购商品
                    if staff_goods_list and len(staff_goods_list) != len(goods_list):
                        mix_staff_and_goods = True
                # 获取只需要的商品信息
                result = []  # 存放结果
                for goods in goods_list:
                    goods_info = {}
                    if current_user.is_staff:
                        for item in staff_goods_list:
                            if goods.goods_id == item.goods_id:
                                goods.current_price = item.price
                                break
                    if goods_id == goods.goods_id:
                        if goods.sale_type == "new_buyer":
                            new_buyer_count += int(count)
                        goods_info["id"] = goods_id
                        goods_info["count"] = count
                        goods_info["price"] = str(goods.current_price)
                        goods_info["img"] = self.build_photo_url(goods.img_view, pic_type="goods", cdn=True)
                        goods_info["title"] = goods.goods_title
                        goods_info["total_price"] = goods.current_price * int(count)
                        result.append(goods_info)
                        sum_price += goods_info["total_price"]
                        break

        # 判断是否是享有新人商品
        if new_buyer_count == 1:
            orders = [o for o in Order.get_order_by_member_id(member_id)]
            if not orders:
                # 没有下过订单
                is_newbuyer = True
            else:
                # 下过单，付过款
                for each in orders:
                    if each.status in ["2", "3", "4"]:
                        is_newbuyer = False

        avali_coupons, max_coupon = self.get_avali_coupons(sum_price)

        self.render("www/w_order_confirm.html",
                    category_list=category_list, address_list=address_list,
                    max_coupon=max_coupon, result=result,default_address=default_address,
                    sum_price=sum_price, avali_coupons=avali_coupons, current_user=current_user,
                    new_buyer_count =new_buyer_count, is_newbuyer=is_newbuyer,
                    mix_staff_and_goods=mix_staff_and_goods, staff_goods_list=staff_goods_list)

    def get_avali_coupons(self, sum_price):
        avail_coupon_list = Coupon.list_coupons_by_status("unused", self.current_user.member_id,
                                                          int(time.time()), api_use="can_use",
                                                          price=float(sum_price))
        coupons = []
        max_coupon = {"id": None, "face_value": 0}
        if avail_coupon_list:
            for each in avail_coupon_list:
                coupon_dict = dict()
                coupon_dict["face_value"] = str(each.face_value)
                coupon_dict["coupon_set_name"] = each.coupon_set_name
                coupon_dict["use_condition"] = str(each.use_condition)
                coupon_dict["avail_start_at"] = each.avail_start_at
                coupon_dict["avail_end_at"] = each.avail_end_at
                coupon_dict["coupon_id"] = each.coupon_id
                coupon_dict["avail"] = 1
                if max_coupon['face_value'] < each.face_value:
                    max_coupon['face_value'] = each.face_value
                    max_coupon['id'] = each.coupon_id
                coupons.append(coupon_dict)

        return coupons, max_coupon


class WwwOrderPayHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        status = self.get_argument("status", "0")
        order_id = self.get_argument("order_id", None)

        category_list = self.get_category()

        member_id = self.current_user.member_id
        order = Order.load_my_order_by_id(member_id, order_id)

        ordergoods_list = OrderGoods.list_order_goods_by_order_id(order_id)
        if ordergoods_list:
            goods_id_list = [each.goods_id for each in ordergoods_list]
            goods_list = Goods.find_order_goods_list(goods_id_list)

        order_info = {"goods_list": []}
        # body = ""
        for order_goods in ordergoods_list:
            if order.order_id == order_goods.order_id:
                for goods in goods_list:
                    info = {}
                    if goods.goods_id == order_goods.goods_id:
                        info["count"] = order_goods.goods_count
                        info["title"] = goods.goods_title
                        info["goods_id"] = goods.goods_id
                        info["price"] = str(goods.current_price)
                        # body += goods.goods_title + "\n"
                        order_info["goods_list"].append(info)
                        break

        # 判断订单中有没有专享商品，然后决定能不能去支付
        is_newbuyer = False
        message = ""
        sale_status = "success"
        if not self.current_user.is_staff:
            sale_status = check_order_is_new_buyer_order(order_id,
                                                         self.current_user.member_id)
        if "success" not in sale_status:
            message = sale_status
        else:
            is_newbuyer = True

        if order.group_buy_id:
            order_l = Order.list_group_buy_order_by_group_buy_id(order.group_buy_id,
                                                          status=["13", "14", "15"])
            if order_l:
                message = u"该拼团购买已经成功"
            else:  # 24小时可能还没有取消，也将不许够买
                order_list = Order.list_group_buy_order_by_group_buy_id(order.group_buy_id)
                if order_list:
                    head_order = order_list[0]
                    end_time = head_order.create_time + timedelta(days=1)
                    timer = 0
                    if end_time > head_order.create_time:
                        timer = (time.mktime(end_time.timetuple()) -
                                 time.mktime(datetime.now().timetuple())) * 1000
                    if timer <= 0:
                        message = u"该拼团购买已经超时"

        if order.status in ["2", "3", "4", "12", "13", "14", "15"]:
            message = u"该订单已经支付完成"

        self._render(category_list, order, order_info["goods_list"], is_newbuyer, message)

    def _render(self, category_list, order, goods_add, is_newbuyer, message):
        if order:
            self.render("www/w_order_pay.html",
                        category_list=category_list, order_id=order.order_id,
                        price=order.price, goods_add=goods_add,
                        collect_address=order.collect_address,
                        collect_person=order.collect_person,
                        collect_tel=order.collect_tel, error=False,
                        is_newbuyer=is_newbuyer, message=message, body="")
        else:
            self.render("www/w_order_pay.html", category_list=category_list,
                        error=True)

    @www_authenticated
    def post(self):
        order_id = self.get_argument("order_id", None)
        pay_way = self.get_argument("pay_way", None)

        member_id = self.current_user.member_id
        order = Order.load_my_order_by_id(member_id, order_id)

        # 判断订单中有没有专享商品，然后决定能不能去支付
        sale_status = "success"
        if not self.current_user.is_staff:
            sale_status = check_order_is_new_buyer_order(order_id,
                                                         self.current_user.member_id)
        if "success" not in sale_status:
            self.redirect("/order/pay?order_id=" + order_id)

        ordergoods_list = OrderGoods.get_order_goods_by_order_id(order_id)
        subject = u"[美会说]"
        body = ""
        if ordergoods_list:
            goods_id_list = [each.goods_id for each in ordergoods_list]
            goods_list = Goods.find_order_goods_list(goods_id_list)
            for goods in goods_list[0:3]:
                if not body:
                    subject += goods.goods_title + u"等"
                    body = goods.goods_title
                else:
                    body += "," + goods.goods_title

        if pay_way == "alipay":
            pay_params = {}
            pay_params["partner"] = self.settings["alipay_partner"]
            pay_params["notify_url"] = "http://api.meihuishuo.com/callback/alipay_notify/"
            pay_params["return_url"] = "http://api.meihuishuo.com/callback/alipay_return/"
            pay_params["total_fee"] = str(order.price)
            pay_params["out_trade_no"] = str(order_id)
            pay_params["seller_id"] = self.settings["alipay_seller_id"]
            pay_params["body"] = body.encode("utf-8")
            pay_params["subject"] = subject[0:128].encode("utf-8")
            pay_params['service'] = "create_direct_pay_by_user"
            pay_params['_input_charset'] = "utf-8"
            pay_params['payment_type']  = "1"
            pay_params['paymethod'] = "directPay"
            pay_params["it_b_pay"] = "60m"

            params, prestr = params_filter(pay_params)
            params['sign'] = md5(prestr + self.settings["alipay_sign_key"]).hexdigest()
            params["sign_type"] = "MD5"
            url = self.settings["alipay_gateway_url"] + urlencode(params)

            self.redirect(url)
        elif  pay_way == "wxpay":
            category_list = self.get_category()
            pay_params = {}
            pay_params["appid"] = self.settings["wxpay_code_appid"]
            pay_params["mch_id"] = self.settings["wxpay_code_partnerid"]
            pay_params["device_info"] = "WEB"
            pay_params["body"] = "[美会说药妆海外购]订单编号"+order_id
            pay_params["detail"] = body
            pay_params["out_trade_no"] = str(order_id)
            pay_params["total_fee"] = str(int(float(order.price)*100))
            pay_params["spbill_create_ip"] = self.client_ip  # 用户 IP
            pay_params["notify_url"] = self.settings["wxpay_code_notify_url"]
            pay_params["trade_type"] = "NATIVE"
            pay_params["nonce_str"] = lib_common.random_str()
            pay_params["product_id"] = str(order_id)

            _, prestr = params_filter(pay_params)
            stringSignTemp = "{0}&key={1}".format(prestr, self.settings["wxpay_code_sign_key"])
            stringSignTemp = md5(stringSignTemp).hexdigest()
            pay_params["sign"] = stringSignTemp.upper()
            request_str = lib_common.dict_to_xml(pay_params)
            response_body = self.unified_order(request_str)
            response = lib_common.xml_to_dict(response_body)
            error = True
            qr_code_url = address = qr_code = phone = person = ""
            if "return_code" not in response and \
                "result_code" not in response:
                # 统一下单失败接口调用失败
                self.wx_prepay_log(response, order, "接口调用失败")
            elif response["return_code"] != "SUCCESS":
                # 通信失败, 统一下单失败接口调用失败
                self.wx_prepay_log(response, order, response["return_msg"])
            elif response["return_code"] == "SUCCESS" and \
                response["result_code"] != "SUCCESS":
                # 通信成功交易失败
                self.wx_prepay_log(response, order, response["err_code_des"])
            elif response["return_code"] == "SUCCESS" and \
                response["result_code"] == "SUCCESS":
                # 交易成功, 页面生成二维码，然用户扫描支付
                error = False
                qr = response["code_url"]
                qr_code_url = qrcode.make(qr)
                img_io = StringIO.StringIO()
                qr_code_url.save(img_io)  # 直接将生成的QR放在了内存里
                img_io.seek(0)
                qr_code = "data:image/png;base64,"+base64.b64encode(img_io.read())   # 生成二维码的base64
                address = order.collect_address
                phone = order.collect_tel
                person = order.collect_person
                self.wx_prepay_log(response, order)

            self._render_wx(category_list, error, order_id,
                            order.price, qr_code_url, body,
                            address, phone, person, qr_code)

    def _render_wx(self, category_list, error, order_id,
                   price, qr_code_url, body, address,
                   phone, person, qr_code):
        self.render("www/wxpay.html",
                    error=error, order_id=order_id, price=price, qr_code=qr_code,
                    qr_code_url=qr_code_url, body=body,  address=address,
                    phone=phone, person=person, category_list=category_list)

    def wx_prepay_log(self, response, order, error_mes=""):
        prepay_log = dict()
        prepay_log["trade_status"] = "prepare_pay"
        prepay_log["sign_type"] = "MD5"
        prepay_log["pay_type"] = "weixin"
        prepay_log["out_trade_no"] = order.order_id
        prepay_log["error_message"] = error_mes
        prepay_log["return_data"] = str(response)
        prepay_log["create_at"] = int(time.time())
        prepay_log["total_fee"] = order.price
        prepay_log["pay_result"] = "Y" if not error_mes else "N"
        prepay_log["trade_no"] = response["prepay_id"] if \
            "prepay_id" in response and response["prepay_id"] else ""
        prepay_log["sign"] = response["sign"] if \
            "sign" in response and response["sign"] else ""
        prepay_log["buyer_id"] = self.current_user.member_id
        prepay_log["before_order_status"] = order.status
        prepay_log["payment_type"] = "weixin"
        order_model.PayLog.insert_pay_log(prepay_log)
        return

    def unified_order(self, xml_str):
        headers = {
            "Content-type": "application/xml",
            "Content-Length": "%d" % len(xml_str)
        }
        try:
            req = urllib2.Request(
                url="https://api.mch.weixin.qq.com/pay/unifiedorder",
                data=xml_str, headers=headers
            )
            res_data = urllib2.urlopen(req)
            return res_data.read()
        except Exception:
            return None


class WwwOrderStatusCheckHandler(WwwBaseHandler):
    """支付前检查订单状态
    """
    def post(self):
        order_id = self.get_argument("order_id", None)
        order = None
        if order_id:
            order = Order.load_order_by_id(order_id)

        if not order_id or not order:
            self.data["message"] = "没有查询到该订单，请确认是否存在该订单"
            self.write(self.data)
            return

        if order.status == "1":
            self.data["status"] = "success"
            self.data["status_code"] = "1"
        elif order.status == "2":
            self.data["message"] = "订单已经付款，等待发货"
            self.data["status_code"] = "2"
        elif order.status == "3":
            self.data["message"] = "订单已经付款，等待收货"
            self.data["status_code"] = "3"
        elif order.status == "4":
            self.data["message"] = "订单已经付款，并且已经收货"
            self.data["status_code"] = "4"
        elif order.status == "10":
            self.data["message"] = "订单已经被关闭，请重新下单"
            self.data["status_code"] = "10"
        elif order.status == "11":
            self.data["status"] = "success"
            self.data["message"] = "未支付，未成团"
            self.data["status_code"] = "11"
        elif order.status == "12":
            self.data["message"] = "已支付，未成团"
            self.data["status_code"] = "12"
        elif order.status == "13":
            self.data["message"] = "已支付，待发货"
            self.data["status_code"] = "13"
        elif order.status == "14":
            self.data["message"] = "已成团，待收货"
            self.data["status_code"] = "14"
        elif order.status == "15":
            self.data["message"] = "已成团，待评价"
            self.data["status_code"] = "15"
        elif order.status == "16":
            self.data["message"] = "未成团，已退款"
            self.data["status_code"] = "16"

        self.write(self.data)


class WwwOrderPayStatusHandler(WwwBaseHandler):
    def get(self, order_id):
        category_list = self.get_category()
        if order_id:
            order = Order.load_order_by_id(order_id)
            total_fee = order.price
            msg = "支付异常"
            if order.status != "1":
                msg = "支付成功"

            ordergoods_list = OrderGoods.get_order_goods_by_order_id(order_id)
            subject = ""
            if ordergoods_list:
                goods_id_list = [each.goods_id for each in ordergoods_list]
                goods_list = Goods.find_order_goods_list(goods_id_list)
                for goods in goods_list:
                    subject = goods.goods_title + u"等"
                    break

        self.render("www/w_order_pay_return.html",
                     total_fee=total_fee,  out_trade_no=order_id, subject=subject,
                    msg=msg, category_list=category_list)


urls = [
    (r"/order/confirm/?", WwwOrderConfirmHandler),
    (r"/order/pay/?", WwwOrderPayHandler),
    (r"/order/payment/(.*?)/?", WwwOrderPayStatusHandler),
    (r"/order/status/?", WwwOrderStatusCheckHandler),
]

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import tornado.web
import time

from meihuishuo.libs.decorators import www_authenticated
from meihuishuo.libs.handlers import WwwBaseHandler, JsWwwBaseHandler
from meihuishuo.models.coupon_model import Coupon, CouponSet
from meihuishuo.models.member_model import Member


class WMyCouponHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        category_list = self.get_category()
        status = self.get_argument("status", None)

        if not status:
            status = "unused"

        coupon_list = Coupon.list_coupons_by_status(status,
                                                    self.current_user.member_id,
                                                    int(time.time()))
        coupons =[]
        if coupon_list:
            for coupon in coupon_list:
                coupon_dict = {}
                coupon_dict["coupon_set_name"] = coupon.coupon_set_name
                coupon_dict["face_value"] = str(coupon.face_value)
                coupon_dict["use_condition"] = str(coupon.use_condition)
                coupon_dict["avail_start_at"] = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(coupon.avail_start_at))
                coupon_dict["avail_end_at"] = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(coupon.avail_end_at))
                coupon_dict["coupon_id"] = coupon.coupon_id
                coupons.append(coupon_dict)

        self.render("www/w_my_coupon.html",
                    status=status, coupons=coupons,
                    category_list=category_list)


class WRedeemCouponHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        code = self.get_argument("coupon_code", None)
        if not code:
            self.data["message"] = "没有优惠券"
            self.write(self.data)
            return

        coupon = Coupon.load_coupon_by_code(code)
        if not coupon:
            self.data["message"] = "没有该优惠券"
            self.write(self.data)
            return

        coupon_set = CouponSet.load_coupon_set_by_id(coupon.coupon_set_id)
        if not coupon_set:
            self.data["message"] = "优惠券已过期"
            self.write(self.data)
            return

        coupon_count = Coupon.load_coupon_count(coupon_set.coupon_set_id,
                                                self.current_user.member_id)
        if coupon_count >= coupon_set.limit_per_user:
            self.data["message"] = "你已经领取过优惠券了"
            self.write(self.data)
            return

        if coupon.owner_id:
            self.data["message"] = "优惠券已被领取"
            self.write(self.data)
            return

        coupon.owner_id = self.current_user.member_id
        coupon.dist_time = int(time.time())
        coupon.save()

        self.data["result"] = "success"
        self.write(self.data)


class WwwAvailCouponsHandler(JsWwwBaseHandler):
    @www_authenticated
    def get(self):
        price = self.get_argument("price", None)
        if not price:
            self.data["result"] = "error"
            self.data["message"] = "没有可用优惠券"
            self.write(self.data)
            return

        avail_coupon_list = Coupon.list_coupons_by_status("unused", self.current_user.member_id,
                                                          int(time.time()), api_use="can_use",
                                                          price=float(price))
        coupons = []
        if avail_coupon_list:
            for each in avail_coupon_list:
                coupon_dict = dict()
                coupon_dict["face_value"] = str(each.face_value)
                coupon_dict["coupon_set_name"] = each.coupon_set_name
                coupon_dict["use_condition"] = str(each.use_condition)
                coupon_dict["avail_start_at"] = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(each.avail_start_at))
                coupon_dict["avail_end_at"] = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(each.avail_end_at))
                coupon_dict["coupon_id"] = each.coupon_id
                coupon_dict["avail"] = 1
                coupons.append(coupon_dict)

        self.data["result"] = "success"
        self.data["coupons"] = coupons
        self.write(self.data)


urls = [
    (r"/my_coupon/?", WMyCouponHandler),
    (r"/my_conpon/redeem/?", WRedeemCouponHandler),
    (r"/my_conpon/available/?", WwwAvailCouponsHandler),
]
#!/usr/bin/env python
# coding:utf-8


import time
import json
import string
import random
import uuid
import urllib
import datetime

from meihuishuo.libs.handlers import JsWwwBaseHandler
import meihuishuo.libs.social_sdk as social_sdk
import meihuishuo.models.member_model as member_model
import meihuishuo.libs.coupon as lib_coupon
import meihuishuo.models.shop_cart_model as shop_cart_model
import meihuishuo.models.goods_model as goods_model


class SociallLoginHandler(JsWwwBaseHandler):
    def get(self):
        code = self.get_argument("code", None)
        social_type = self.get_argument("provider", "")
        if code:
            call_bacl_url = 'http://www.meihuishuo.com/callback/sociallogin?provider=' + social_type
            client = user_info =  None
            if social_type == "sina":
                client = social_sdk.WeiboAPIClient(app_key=self.settings["weibo_app_key"],
                                                   app_secret=self.settings["weibo_app_secret"],
                                                   redirect_uri=call_bacl_url)
                r = client.request_access_token(code)
                client.set_access_token(r.access_token, r.expires_in)
                user_info = client.users.show.get(access_token=r.access_token, uid=r.uid)

            elif social_type == "qq":
                client = social_sdk.QQAPIClient(app_key=self.settings["qq_app_id"],
                                                app_secret=self.settings["qq_app_key"],
                                                redirect_uri=call_bacl_url)
                r = client.request_access_token(code, access_token="token")
                client.set_access_token(r.access_token, r.expires_in)
                user_info = client.user.get_user_info.get(access_token=r.access_token,
                                                          openid=client.get_openid(),
                                                          uid=r.uid)

            elif social_type == "weixin":
                client = social_sdk.WeixinAPIClient(app_key=self.settings["weixin_web_id"],
                                                app_secret=self.settings["weixin_web_key"],
                                                redirect_uri=call_bacl_url)
                r = client.request_access_token(code, access_token="access_token")
                client.set_access_token(r.access_token, r.expires_in)
                user_info = client.userinfo.get(access_token=r.access_token,
                                                    openid=r.openid)

            if not client:
                self.redirect("/")
                return

            if social_type == "weixin":
                social_type = "wechat"
                member = member_model.Member.load_other_platform_member(user_info.openid, platform=social_type)
            elif social_type == "sina":
                member = member_model.Member.load_other_platform_member(user_info.id, platform=social_type)
            elif social_type == "qq":
                member = member_model.Member.load_other_platform_member(r.openid, platform=social_type)

            if not member:
                member = member_model.Member()

                if social_type == "sina":
                    member.wb_openid = user_info.id
                    if user_info.gender == "m":
                        member.sex = "男"
                    elif user_info.gender == "f":
                        member.sex = "女"
                    else:
                        member.sex = "未知"
                    member.member_name = user_info.screen_name
                    member.member_avatar = user_info.profile_image_url

                elif social_type == "qq":
                    member.qq_openid = r.openid
                    if user_info.gender == "1":
                        member.sex = "男"
                    elif user_info.gender == "2":
                        member.sex = "女"
                    else:
                        member.sex = "未知"
                    member.member_name = user_info.nickname
                    member.member_avatar = user_info.figureurl_qq_1

                elif social_type == "wechat":
                    member.wx_openid = user_info.openid
                    if user_info.sex == "1":
                        member.sex = "男"
                    elif user_info.sex == "2":
                        member.sex = "女"
                    else:
                        member.sex = "未知"
                    member.member_name = user_info.nickname
                    member.member_avatar = user_info.headimgurl

                now_time = datetime.datetime.now()
                member.member_id = str(uuid.uuid4()).replace("-", "")
                member.member_id = member.member_id[0:15]
                member.create_time = now_time
                member.update_time = now_time
                member.access_token = r.access_token
                member.created_ip = self.client_ip
                member.status = "1"
                member.save(force_insert=True)

                coupon_sum_value = 0
                coupon_sets = lib_coupon.gen_coupon_by_condition(condition="register",
                                                                 member_id=member.member_id)
                if coupon_sets:
                    for each in coupon_sets:
                        coupon_sum_value = coupon_sum_value + each.face_value

            self.login_session(member)

        self.redirect("/")


    def login_session(self, member, merge_cart=True):
        sess_key = ''.join(random.choice(string.lowercase + string.digits)
                           for i in range(10)
                           )
        session = {"id": sess_key, "time": int(time.time())}

        try:
            sessions = json.loads(member.sessions)
        except:
            sessions = list()
        if not isinstance(sessions, list):
            sessions = list()
        sessions.append(session)

        if len(sessions) > 5:
            sessions = sessions[-5:]

        member.sessions = json.dumps(sessions)
        member.save()

        # 合并登录前的购物车
        if merge_cart:
            self.merge_shopcart(member)

        self.clear_cookie(self.LOGIN_NEXT)

        self.set_cookie(self.settings["cookie_key_sess"],
                        member.member_id + ":" + sess_key)

    def merge_shopcart(self, member):
        #
        # 合并购物车
        #
        try:
            mhs_cart = urllib.unquote(self.get_cookie("mhs-cart"))
        except Exception as e:
            mhs_cart = None
        if mhs_cart:
            cart = json.loads(mhs_cart)
            items = cart['items']
            if items:
                goods_ids = []
                shopcart_goods_map = {}
                shocart_list = shop_cart_model.ShopCart.get_app_cart_goods_list(member.member_id)
                for cart in shocart_list:
                    goods_ids.append(cart.goods_id)
                    shopcart_goods_map[cart.goods_id] = cart

                cart_list = []  # 新添加的购物车
                update_list = []  # 需要更新的购物车信息
                create_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
                for item in items:
                    if item['GoodsId'] not in goods_ids:
                        # 数据库没有该购物车商品
                        cart_dict = dict()
                        goods = goods_model.Goods.get_goods_by_goods_id(item['GoodsId'])
                        if goods.sale_type == "new_buyer":
                            cart_dict["goods_count"] = "1"
                        else:
                            cart_dict["goods_count"] = item['Count']
                        create_time = create_time - datetime.timedelta(seconds=1)
                        cart_dict["uuid"] = str(uuid.uuid4())
                        cart_dict["member_id"] = member.member_id
                        cart_dict["goods_id"] = item['GoodsId']
                        cart_dict["create_time"] = create_time
                        cart_list.append(cart_dict)

                if cart_list:
                    shop_cart_model.ShopCart.insert_many_items(cart_list)
                if update_list:
                    shop_cart_model.app_update_cart([], update_list, "new")


urls = [
    (r"/callback/sociallogin/?", SociallLoginHandler),
    ]
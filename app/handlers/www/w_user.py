#!/usr/bin/env python
# coding:utf-8

import uuid
from datetime import datetime

from meihuishuo.libs.handlers import WwwBaseHandler, JsWwwBaseHandler
from meihuishuo.models.member_model import Member, Address
from meihuishuo.libs.decorators import www_authenticated
from meihuishuo.models.goods_model import Goods, HomeLimitedGoods, Collection, Country, CurrencyType


class WAccountSecurityHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        category_list = self.get_category()
        member_id = self.current_user.member_id
        member = Member.load_member_by_member_id(member_id)

        member_info = {"member_name": "", "sex": ""}
        member_info["member_name"] = member.member_name
        member_info["sex"] = member.sex
        member_info["birthday"] = member.birthday
        member_info["hash_pwd"] = member.hash_pwd
        member_info["telephone"] = member.telephone

        self.render("www/w_account_security.html",
                    member_info=member_info, category_list=category_list)


class WMyFavoriteHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        category_list = self.get_category()

        member_id = self.current_user.member_id
        goods = []

        goods_ids = [each.related_id for each in
                     Collection.select().where(Collection.member_id == member_id)
                               .order_by(Collection.create_time.desc())]
        if not goods_ids:
            self.render("www/w_my_favorite.html", goods=goods,
                        category_list=category_list)

        goods_list = [each for each in
                      Goods.select().where(Goods.goods_id.in_(goods_ids))]
        limited_goods_list = [each for each in
                              HomeLimitedGoods.list_limited_goods_by_goods_ids(goods_ids)]

        country_list = [each for each in Country.list_countries()]
        current_type_list = [each for each in CurrencyType.list_currency_type()]

        for goods_id in goods_ids:
            for each in goods_list:
                goods_dict = dict()
                if goods_id == each.goods_id:
                    for limited_goods in limited_goods_list:
                        if each.goods_id == limited_goods.goods_id:
                            each.stock = limited_goods.goods_left_count
                            break

                    goods_dict["goods_id"] = each.goods_id
                    goods_dict["goods_img_url"] = self.build_photo_url(each.img_view, pic_type="goods", cdn=True)
                    goods_dict["buy_count"] = int(each.buy_count)
                    goods_dict["goods_title"] = each.goods_title
                    goods_dict["price"] = str(each.current_price)
                    goods_dict["stock_count"] = int(each.stock) if each.stock else 1
                    goods_dict["goods_brief_intro"] = each.abbreviation
                    goods_dict["overseas_price"] = each.overseas_price
                    goods_dict["domestic_price"] = each.domestic_price
                    goods_dict["foreign_price"] = each.foreign_price
                    goods_dict["symbol"] = "￥"
                    goods_dict["country_name"] = each.origin
                    goods_dict["country_img_url"] = ""
                    for c_t in current_type_list:
                        if each.foreign_type == c_t.uuid:
                            goods_dict["symbol"] = c_t.symbol
                            break
                    for country in country_list:
                        if country.country_cn_name in each.origin:
                            goods_dict["country_name"] = country.country_cn_name
                            goods_dict["country_img_url"] = self.build_country_img_url(country.country_id)
                            break
                    goods.append(goods_dict)

        self.render("www/w_my_favorite.html", goods=goods,
                    category_list=category_list)


class WMyAddressHandler(WwwBaseHandler):
    @www_authenticated
    def get(self):
        category_list = self.get_category()
        member_id = self.current_user.member_id

        address = Address.find_all(member_id)

        default_address_id = self.current_user.default_address_id
        default_address = None
        address_list = []
        for each in address:
            if each.address_id == default_address_id:
                default_address = {}
                default_address["address_id"] = each.address_id
                default_address["collect_address"] = each.address
                default_address["collect_person"] = each.addressee
                default_address["telephone"] = each.telephone
                default_address["area"] = each.area
            else:
                each_dict = {}
                each_dict["address_id"] = each.address_id
                each_dict["collect_address"] = each.address
                each_dict["collect_person"] = each.addressee
                each_dict["telephone"] = each.telephone
                each_dict["area"] = each.area
                address_list.append(each_dict)

        self.render("www/w_my_address.html",
                    address_list=address_list, category_list=category_list,
                    default_address=default_address)


class WJsAddAddressHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        area = self.get_argument("area", None)
        detail_address = self.get_argument("detail_address", None)
        receiver_name = self.get_argument("receiver_name", None)
        telephone = self.get_argument("telephone", None)
        member_id = self.current_user.member_id

        if not member_id or not area or not detail_address or \
           not receiver_name or not telephone:
            self.data["message"] = "请补全信息"
            self.write(self.data)
            return

        addresses = Address.list_address_by_member_id(self.current_user.member_id)
        no_address = False
        if not addresses:
            no_address = True

        address = Address()
        address.addressee = receiver_name
        address.address = detail_address
        address.telephone = telephone
        address.member_id = member_id
        address.area = area
        address.address_id = str(uuid.uuid4())
        address.create_time = datetime.now()
        address.update_time = datetime.now()
        address.save(force_insert=True)

        if no_address:
            default_address_id = address.address_id
            Member.update_member_by_member_ids([self.current_user.member_id],
                                                       {"default_address_id": default_address_id})

        self.data["result"] = "success"
        self.data["address_id"] = address.address_id
        self.write(self.data)


class WJsUpdateAddressHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        address_id = self.get_argument("address_id", None)
        area = self.get_argument("area", None)
        detail_address = self.get_argument("detail_address", None)
        receiver_name = self.get_argument("receiver_name", None)
        telephone = self.get_argument("telephone", None)
        member_id = self.current_user.member_id

        if not member_id or not area or not detail_address or \
           not receiver_name or not telephone or not address_id:
            self.data["message"] = "请补全信息"
            self.write(self.data)
            return

        address = Address.find_by_id(address_id)
        if not address:
            self.data["result"] = "error"
            self.data["message"] = "请求出错"
            self.write(self.data)
            return

        address.addressee = receiver_name
        address.address = detail_address
        address.telephone = telephone
        address.area = area
        address.update_time = datetime.now()
        address.save()

        self.data["result"] = "success"
        self.write(self.data)


class WJsDeleteAddressHandler(JsWwwBaseHandler):
    @www_authenticated
    def post(self):
        address_id = self.get_argument("address_id", None)

        if address_id:
            Address.delete_by_id(address_id)
            # 将最近的地址设置为默认地址
            if self.current_user.default_address_id == address_id:
                addresses = Address.list_address_by_member_id(self.current_user.member_id)
                if addresses:
                    default_address_id = addresses[0].address_id
                    Member.update_member_by_member_ids([self.current_user.member_id],
                                                       {"default_address_id": default_address_id})
            self.data["result"] = "success"
        else:
            self.data["message"] = "地址不存在"

        self.write(self.data)


class WJsDefaultAddressHandler(JsWwwBaseHandler):
    @www_authenticated
    def patch(self):
        """设置默认收货地址"""
        address_id = self.get_argument("address_id", "")
        if not address_id:
            self.data["message"] = "请选择相应的地址"
            self.write(self.data)
            return

        Member.update_member_by_member_ids([self.current_user.member_id],
                                           {"default_address_id": address_id})

        self.data["result"] = "success"
        self.write(self.data)


urls = [
    (r"/account_security/?", WAccountSecurityHandler),
    (r"/my_favorite/?", WMyFavoriteHandler),
    (r"/my_address/?", WMyAddressHandler),
    (r"/my_address/delete/?", WJsDeleteAddressHandler),
    (r"/my_address/add/?", WJsAddAddressHandler),
    (r"/my_address/update/?", WJsUpdateAddressHandler),
    (r"/my_address/default/?", WJsDefaultAddressHandler),
]

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from meihuishuo.libs.handlers import SiteBaseHandler
from meihuishuo.models.goods_model import Goods, CurrencyType, \
    Brand, Effect, GoodsImg, Country, GoodspecificationType
from meihuishuo.models.home_model import Shop


class MShrareGoosHandler(SiteBaseHandler):
    def get(self, goods_id):
        goods = Goods.get_goods_by_goods_id(goods_id)
        if not goods:
            self.send_error(404)
            return

        goods_detail = {}
        symbol = CurrencyType.get_symbol(goods.foreign_type)
        good_effects = Effect.find_effect_by_id(goods_id)
        brand = Shop.find_shop_img_by_shop_id(goods.shop_id)
        specifications_type_name = GoodspecificationType.get_goodspecification_type_name(goods.specifications_type)
        if brand:
            country = Country.get_country(brand.country_id)
            goods_detail["country"] = country.country_cn_name + \
                " / " + country.country_en_name
        else:
            goods_detail["country"] = ""

        effect_value = ""
        if good_effects:
            for good_effect in good_effects:
                effect_value = effect_value + " " + \
                    good_effect.effect_title
            effect_value = effect_value[1: len(effect_value)]

        goods_img = GoodsImg.find_goods_img_by_id(goods_id)
        img_list = []
        for img in goods_img:
            img_url = self.build_photo_url(img.img_view, pic_type="goods", cdn=True)
            img_list.append(img_url)

        # if '.' not in goods.domestic_price:
        #     domestic_price = str(goods.domestic_price)+".00"
        # else:
        #     domestic_price = str(goods.domestic_price)

        goods_detail["domestic_price"] = str(goods.domestic_price)
        goods_detail["overseas_price"] = symbol + str(goods.foreign_price)
        goods_detail["specifications"] = goods.specifications + specifications_type_name
        if brand:
            if brand.brand_cn_name != brand.brand_en_name:
                goods_detail["brand"] = brand.brand_cn_name + "/" + \
                    brand.brand_en_name
            else:
                goods_detail["brand"] = brand.brand_cn_name
        else:
            goods_detail["brand"] = ""
        goods_detail["effect"] = effect_value
        goods_detail["img_urls"] = img_list

        self.render("m_mobile/m_share.html",
                    goods=goods, goods_detail=goods_detail)


urls = [
    (r"/goods_share/([a-z0-9-]+)/?", MShrareGoosHandler),
]

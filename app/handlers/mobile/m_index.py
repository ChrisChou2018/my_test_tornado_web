# -*- coding: utf-8 -*-

from time import mktime, time

from meihuishuo.libs.handlers import WwwBaseHandler
from meihuishuo.models.goods_model import HomeLimitedGoods, Goods, Country
from meihuishuo.models.home_model import Shop

class MIndexHandler(WwwBaseHandler):
    def get(self):
        essence_list = self.get_essence_goods()
        # figure_pics = self.get_home_figure_pic()
        figure_pics = self.get_home_slider()

        self.render("m_mobile/m_index.html",
                    essence_list=essence_list, figure_pics=figure_pics)

    def get_essence_goods(self):
        goods_list = [each for each in
                        HomeLimitedGoods.list_home_goods(None,'home_essence')]
        result = self.get_goods_info(goods_list) if goods_list else []

        return result

    def get_home_figure_pic(self):
        """获取首页广告轮番图
        """
        figure_list = HomeLimitedGoods.list_advertisement_goods(None,
                                                                "adv_parent",
                                                                "api")
        adv_list = []
        for each in figure_list:
            adv_info = {}
            adv_info["id"] = each.limited_id
            pic_ids = []
            if each.goods_pic_id:
                pic_ids = each.goods_pic_id.split(",")

            if not pic_ids or not pic_ids[0]:
                continue

            adv_info["adv_img_url"] = self.build_photo_url(pic_ids[0], pic_version="title",
                                                           pic_type="goods", cdn=True)
            adv_list.append(adv_info)

        return adv_list

    def get_home_slider(self):
        """获取首页广告轮番图"""
        slide_list = HomeLimitedGoods.list_slides(promo_type=["slide_list", "slide_url", "slide_goods"],
                                                  limited_status="on")
        slides = []
        for each in slide_list:
            slide_dict = dict()

            pic_ids = []
            if each.goods_pic_id:
                pic_ids = each.goods_pic_id.split(",")

            if len(pic_ids) == 2 and pic_ids[1]:
                slide_dict["adv_img_url"] = self.build_photo_url(pic_ids[0], pic_version="title",
                                                                 pic_type="goods", cdn=True)

                if each.promo_type == "slide_list":
                    slide_dict["url"] = "/adv/" + str(each.limited_id)

                elif each.promo_type == "slide_url":
                    slide_dict["url"] = each.goods_id

                elif each.promo_type == "slide_goods":
                    slide_dict["url"] = "/goods/" + each.goods_id
                slides.append(slide_dict)
            else:
                continue

        return slides


    def get_goods_info(self, limit_goods, goods_type=None):
        """获取产品信息
        """
        goods_ids = [each.goods_id for each in limit_goods]
        limited_goods = HomeLimitedGoods.list_limited_goods_by_goods_ids(goods_ids)
        goods_list = Goods.find_order_goods_list(goods_ids)

        shop_ids = shop_list = []
        if goods_list:
            shop_ids = [each.shop_id for each in goods_list]
            shop_list = Shop.get_country_by_shop_id_list(shop_ids)
        countrys = Country.list_countries()

        limited_goods_list = []
        for item in limit_goods:
            goods_info = {}
            for l_goods in limited_goods:
                if l_goods.goods_id == item.goods_id:
                    item = l_goods
                    break

            for goods in goods_list:
                if item.goods_id == goods.goods_id:
                    brand = Shop.find_shop_img_by_shop_id(goods.shop_id)
                    if brand and brand.brand_cn_name != brand.brand_en_name:
                        goods_info["brand"] = brand.brand_cn_name + "/" + \
                            brand.brand_en_name
                    else:
                        goods_info["brand"] = brand.brand_cn_name

                    goods_info["price"] = str(goods.current_price)
                    goods_info["goods_intro"] = goods.goods_intro

                    for shop in shop_list:
                        if goods.shop_id == shop.shop_id:
                            for country in countrys:
                                if shop.country_id == country.country_id:
                                    goods_info["country_img_url"] = self.build_country_img_url(
                                        country.country_id
                                    )
                                    goods_info["country"] = country.country_cn_name
                                    break
                            break

                    break  # 找到后停止循环，减少不必要的资源消耗
            try:
                goods_info["limited_end_at"] = float(mktime(item.limited_end_at.timetuple()) - time())*1000
            except:
                goods_info["limited_end_at"] = "0"
            goods_info["id"] = item.goods_id
            goods_info["title"] = item.goods_name
            goods_info["domestic_price"] = str(item.goods_domestic_price)
            goods_info["img_url"] = self.build_photo_url(item.goods_pic_id, pic_version="smdl", pic_type="goods", cdn=True)
            limited_goods_list.append(goods_info)

        return limited_goods_list


urls = [
    (r"/", MIndexHandler),
]
#!/usr/bin/env python
# coding:utf-8

from datetime import datetime, timedelta
from time import mktime, time

from meihuishuo.libs.handlers import WwwBaseHandler
import meihuishuo.models.home_model as home_model
import meihuishuo.models.goods_model as goods_model
import config_web

# Type parent id


class WWWIndexHandler(WwwBaseHandler):
    def get(self):
        category_list = self.get_category()
        recommend_list = self.get_recommend()
        limited_goods_list, next_start_stamp = self.get_limited_goods()
        essence_goods_list = self.get_essence_goods()
        # figure_pics = self.get_home_figure_pic()  # 弃用
        figure_pics = self.get_home_slider()

        self.render("www/w_index.html",
                    category_list=category_list,
                    recommend_list=recommend_list,
                    limited_goods_list=limited_goods_list,
                    essence_goods_list=essence_goods_list,
                    figure_pics=figure_pics,
                    next_start_stamp=next_start_stamp,
                    index=True, id=None, parent=None)

    def get_recommend(self):
        """新品推荐
        """
        recommend_new = goods_model.HomeLimitedGoods.list_home_goods(promo_type="home_new")

        new_goods_list = []
        if recommend_new:
            new_goods_list = self.get_goods_info(recommend_new)

        return new_goods_list

    def set_limited_goods_price(self, goods_list):
        """设置最低价格
        """
        if not goods_list:  return goods_list

        limited_goods = goods_model.HomeLimitedGoods.list_limited_goods(datetime.now())
        if not limited_goods: return goods_list

        for each in goods_list:
            for goods in limited_goods:
                if goods.goods_id == each["goods_id"]:
                    if float(each["price"]) > goods.goods_limited_price:
                        each["price"] = goods.goods_limited_price
                    break

        return goods_list

    def get_goods_info(self, limit_goods, goods_type=None, limied=False):
        """获取产品信息
        """
        goods_ids = [each.goods_id for each in limit_goods]
        goods_list = goods_model.Goods.find_order_goods_list(goods_ids)

        shop_list = []
        if goods_list:
            shop_ids = [each.shop_id for each in goods_list]
            shop_list = home_model.Shop.get_country_by_shop_id_list(shop_ids)
        countrys = goods_model.Country.list_countries()

        today_limited = goods_model.list_cache_info("today_goods_list")

        limited_goods_list = []
        for item in limit_goods:
            goods_info = {}

            for goods in goods_list:
                if item.goods_id == goods.goods_id:

                    for brand in shop_list:
                        if goods.shop_id == brand.shop_id:

                            goods_info["price"] = str(goods.current_price)
                            goods_info["goods_intro"] = goods.goods_intro

                            for country in countrys:
                                if brand.country_id == country.country_id:
                                    goods_info["country_img_url"] = self.build_country_img_url(
                                        country.country_id
                                    )
                                    goods_info["country"] = country.country_cn_name
                                    break
                            break

                    goods_info["stock_count"] = int(goods.stock)
                    if limied:
                        if goods_info["stock_count"] > item.goods_left_count:
                            goods_info["stock_count"] = item.goods_left_count
                    else:
                        for l_g in today_limited:
                            if l_g["goods_id"] == item.goods_id and \
                                            goods_info["stock_count"] > l_g["goods_left_count"]:
                                goods_info["stock_count"] = l_g["goods_left_count"]
                                break

                    if goods_info["stock_count"] < 1:
                        goods_info["is_sold_out"] = 1
                    else:
                        goods_info["is_sold_out"] = 0

                    break  # 找到后停止循环，减少不必要的资源消耗
            try:
                goods_info["limited_end_at"] = float(mktime(item.limited_end_at.timetuple()) - time())*1000
            except:
                goods_info["limited_end_at"] = 0
            goods_info["id"] = item.goods_id
            goods_info["title"] = item.goods_name
            goods_info["domestic_price"] = str(item.goods_domestic_price)
            goods_info["img_url"] = self.build_photo_url(item.goods_pic_id, pic_version="smdl", pic_type="goods", cdn=True)
            limited_goods_list.append(goods_info)

        return limited_goods_list

    def get_limited_goods(self):
        """获取限时抢购商品
        """

        # 获取当前所处的时间段开始 now_start, 和下一时间段的开始 next_start
        now = datetime.now()
        now_str = now.strftime("%H:%M:%S")
        l_duration = sorted(config_web.limit_duration_list, key=lambda item: item['start'])

        now_start = now_str
        next_start = None
        for item in l_duration:
            if item["start"] <= now_str:
                now_start = item["start"]
            elif not next_start:
                next_start = item["start"]

        if not next_start:
            next_start = datetime.strptime(" ".join([(now+timedelta(days=1)).strftime("%Y-%m-%d"),
                                                     " 00:00:00"]),
                                           "%Y-%m-%d %H:%M:%S")
            next_start_stamp = mktime(next_start.timetuple())-mktime(now.timetuple())
        else:
            next_start = datetime.strptime(" ".join([now.strftime("%Y-%m-%d"), next_start]),
                                           "%Y-%m-%d %H:%M:%S")
            next_start_stamp = mktime(next_start.timetuple())-mktime(now.timetuple())

        now_start_dt = datetime.strptime(" ".join([now.strftime("%Y-%m-%d"), now_start]),
                                         "%Y-%m-%d %H:%M:%S")
        limited_goods = goods_model.HomeLimitedGoods.list_goods_in_duration(now_start_dt)
        goods_list = goods_model.list_goods_info(limited_goods, "started")

        return goods_list[:4], next_start_stamp * 1000

    def get_home_figure_pic(self):
        """获取首页广告轮番图
        """
        figure_list = goods_model.HomeLimitedGoods.list_advertisement_goods(None,
                                                                "adv_parent",
                                                                "api")
        adv_list = []
        for each in figure_list:
            adv_info = {}
            adv_info["id"] = each.limited_id
            pic_ids = []
            if each.goods_pic_id:
                pic_ids = each.goods_pic_id.split(",")
            if len(pic_ids) == 2 and pic_ids[1]:
                adv_info["adv_img_url"] = self.build_photo_url(pic_ids[1], pic_version="fhd",
                                                               pic_type="goods", cdn=True)
            else:
                continue
            adv_list.append(adv_info)

        return adv_list

    def get_home_slider(self):
        """获取首页广告轮番图"""
        slide_list = goods_model.HomeLimitedGoods.list_slides(promo_type=["slide_list", "slide_url", "slide_goods"],
                                                  limited_status="on")
        slides = []
        for each in slide_list:
            slide_dict = dict()

            pic_ids = []
            if each.goods_pic_id:
                pic_ids = each.goods_pic_id.split(",")

            if len(pic_ids) == 2 and pic_ids[1]:
                slide_dict["adv_img_url"] = self.build_photo_url(pic_ids[1], pic_version="fhd",
                                                                 pic_type="goods", cdn=True)

                if each.promo_type == "slide_list":
                    slide_dict["url"] = "/adv/" + str(each.limited_id)

                elif each.promo_type == "slide_url":
                    url = each.goods_id
                    if "mlocal.meihuishuo.com" in url:
                        url = each.goods_id.replace("mlocal.meihuishuo.com", "wwwlocal.meihuishuo.com")

                    slide_dict["url"] = url

                elif each.promo_type == "slide_goods":
                    slide_dict["url"] = "/goods/" + each.goods_id
                slides.append(slide_dict)
            else:
                continue

        return slides

    def get_essence_goods(self):
        goods_list = [each for each in
                        goods_model.HomeLimitedGoods.list_home_goods(None,'home_essence')]
        result = self.get_goods_info(goods_list) if goods_list else []

        return result


urls = [
    (r"/", WWWIndexHandler),
]

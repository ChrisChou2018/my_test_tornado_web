# coding:utf-8

from time import mktime, time
from datetime import datetime, timedelta

import meihuishuo.models.activity_model as activity_model
from meihuishuo.libs.handlers import WwwBaseHandler
from meihuishuo.libs.pagination import Paginator
import meihuishuo.models.goods_model as goods_model
from meihuishuo.models.home_model import Shop
import config_web


class WwwAdBaseHandler(WwwBaseHandler):

    def get_goods_info(self, limit_goods, goods_list):
        """获取产品信息
        """
        # goods_ids = [each.goods_id for each in limit_goods]
        # limited_goods = HomeLimitedGoods.list_limited_goods_by_goods_id(goods_ids)

        shop_ids = shop_list = []
        if goods_list:
            shop_ids = [each.shop_id for each in goods_list]
            shop_list = Shop.get_country_by_shop_id_list(shop_ids)
        countrys = goods_model.Country.list_countries()

        limited_goods_list = []

        today_limited = goods_model.list_cache_info("today_goods_list")
        for item in limit_goods:
            goods_info = {}
            for goods in goods_list:
                if item.goods_id == goods.goods_id:
                    if self.current_user:
                        member_id = self.current_user.member_id
                        collection_count = goods_model.Collection.get_colletion_id_count(member_id, goods.goods_id)
                        if collection_count:
                            goods_info["is_favorite"] = "1"
                        else:
                            goods_info["is_favorite"] = "0"
                    else:
                        goods_info["is_favorite"] = "0"
                    goods_info["price"] = str(goods.current_price)
                    goods_info["goods_intro"] = goods.goods_intro
                    goods_info["buy_count"] = goods.buy_count

                    goods_info["stock_count"] = goods.stock
                    for l_g in today_limited:
                        if l_g["goods_id"] == item.goods_id and \
                                        goods_info["stock_count"] > l_g["goods_left_count"]:
                            goods_info["stock_count"] = l_g["goods_left_count"]
                            break
                    if goods_info["stock_count"] < 1:
                        goods_info["is_sold_out"] = 1
                    else:
                        goods_info["is_sold_out"] = 0

                    goods_info["goods_brief_intro"] = goods.abbreviation
                    goods_info["domestic_price"] = goods.domestic_price
                    goods_info["id"] = goods.goods_id
                    goods_info["img_url"] = self.build_photo_url(goods.img_view, pic_type="goods", cdn=True)
                    goods_info["title"] = goods.goods_title
                    goods_info["country"] = ""
                    goods_info["country_img_url"] = ""
                    goods_info["brand"] = ""
                    goods_info["limited_end_at"] = None
                    brand = Shop.find_shop_img_by_shop_id(goods.shop_id)
                    if brand and brand.brand_cn_name != brand.brand_en_name:
                        goods_info["brand"] = brand.brand_cn_name + "/" + \
                            brand.brand_en_name
                    else:
                        goods_info["brand"] = brand.brand_cn_name

                    for shop in shop_list:
                        if goods.shop_id == shop.shop_id:
                            for country in countrys:
                                if shop.country_id == country.country_id:
                                    goods_info["country_img_url"] = self.build_country_img_url(
                                                                    country.country_id)
                                    goods_info["country"] = country.country_cn_name
                                    break
                            break
                    try:
                        goods_info["limited_end_at"] = mktime(item.limited_end_at.timetuple()) - time()
                    except:
                        goods_info["limited_end_at"] = None

                    limited_goods_list.append(goods_info)

                    break  # 找到后停止循环，减少不必要的资源消耗

        return limited_goods_list


class WwwAdvertiseMentHanlder(WwwAdBaseHandler):
    def get(self, parent_id):
        category_list = self.get_category()
        page_num = self.get_argument("page_num", "1")
        num_of_page = 60
        adv_parent = goods_model.HomeLimitedGoods.load_limited_goods(parent_id, limited_status="on")
        promo_type = "adv_child"
        if adv_parent and adv_parent.promo_type == "slide_list":
            promo_type = "slide_list_child"

        limitgoods_list = goods_model.HomeLimitedGoods.list_advertisement_goods(
                        parent_id, promo_type,
                        start=(int(page_num)-1) * num_of_page,
                        num=num_of_page
                     )
        goods_count = goods_model.HomeLimitedGoods.list_advertisement_goods(parent_id,
                                                                promo_type,
                                                                is_count=True)

        goods_list = []
        if limitgoods_list:
            goods_ids = [goods.goods_id for goods in limitgoods_list]
            if goods_ids:
                goods_l = goods_model.Goods.list_goods_by_ids(goods_ids)
                goods_list = self.get_goods_info(limitgoods_list, goods_l)

        # 获取顶部的图片
        if adv_parent:
            pic_ids = adv_parent.goods_pic_id.split(",")
            topimg_url = self.build_photo_url(pic_ids[1], pic_version="hd",
                                              pic_type="goods", cdn=True)
            category_name = adv_parent.goods_limited_intro

        else:
            topimg_url = category_name = ""

        # 分页
        paginator = Paginator(goods_count, num_of_page)
        page = paginator.page(1)
        pages = paginator.calculate_display_pages(1)
        page_num = paginator.total_pages
        less_than_certain_size = paginator.check_less_than_certain_size()
        page_args = {"page": page, "pages": pages, "page_num": page_num,
                     "less_than_certain_size": less_than_certain_size}

        self.render("www/w_advertisement_goods.html",
                    goods_list=goods_list, parent_id=parent_id, parent="",
                    count=goods_count, page_args=page_args, topimg_url=topimg_url,
                    category_list=category_list, category_name=category_name)

class WwwActivityMentHanlder(WwwAdBaseHandler):

    def get(self, activity_id):
        category_list = self.get_category()
        activity = activity_model.Activity.load_activity_by_activity_id(activity_id)
        if not activity:
            self.send_error(404)
            return

        title = activity.activity_name
        topimg_url = self.build_photo_url(activity.activity_header_pic+'.jpg', 'hd', pic_type='goods', cdn=True)
        activity_goods = goods_model.HomeLimitedGoods.list_activity_goods([activity_id], api="activity")
        goods_ids = [each.goods_id for each in activity_goods]
        goods_list = []
        if goods_ids:
            goods_l = goods_model.Goods.list_goods_by_ids(goods_ids)
            goods_list = self.get_goods_info(activity_goods, goods_l)

        # 分页
        goods_count = len(goods_list)
        paginator = Paginator(goods_count, goods_count)
        page = paginator.page(1)
        pages = paginator.calculate_display_pages(1)
        page_num = paginator.total_pages
        less_than_certain_size = paginator.check_less_than_certain_size()
        page_args = {"page": page, "pages": pages, "page_num": page_num,
                     "less_than_certain_size": less_than_certain_size}

        self.render("www/w_advertisement_goods.html",
                    goods_list=goods_list, parent_id=activity_id, parent="",
                    count=goods_count, page_args=page_args, topimg_url=topimg_url,
                    category_list=category_list, category_name=title)


class WwwLimitBuyHandler(WwwBaseHandler):
    def get(self):
        category_list = self.get_category()
        # 获取天活动的开头与结束
        now = datetime.now()
        duration = self.list_duration()
        now_stamp = mktime(now.timetuple())

        try:
            next_duration = min(duration["soon_start_stamp_list"])
            timer = (next_duration-now_stamp) * 1000  # 下本场剩余时间
        except:
            duration_l = config_web.limit_duration_list
            if duration_l:
                d = duration_l[0]["end"]
            else:
                d = "00:00:00"
            end = mktime(datetime.strptime(" ".join([(now+timedelta(days=1)).strftime("%Y-%m-%d"), d]),
                                      "%Y-%m-%d %H:%M:%S").timetuple())
            timer = (end-now_stamp) * 1000  # 下本场剩余时间

        now_start = " ".join([now.strftime("%Y-%m-%d"), duration["now_start"]])
        limited_goods = goods_model.HomeLimitedGoods.list_goods_in_duration(now_start)
        goods_list = goods_model.list_goods_info(limited_goods)

        self.render("www/w_limitbuy.html",
                    category_list=category_list, goods_list=goods_list,
                    duration_list=duration["duration_list"],
                    now_start_tabid=duration["now_start_tabid"], timer=timer)

    def list_duration(self):
        """获取时间段信息"""
        l_duration = sorted(config_web.limit_duration_list, key=lambda item: item['start'])

        now = datetime.now()
        now_stamp = mktime(now.timetuple())

        duration_list = []
        now_start = now  # 记录当前活动的开头
        now_start_tabid = now_stamp
        soon_start_stamp_list = []
        for duration in l_duration:  # 记录每个阶段的时间等信息
            start = datetime.strptime(" ".join([now.strftime("%Y-%m-%d"), duration["start"]]),
                                      "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(" ".join([(now+timedelta(days=1)).strftime("%Y-%m-%d"), duration["end"]]),
                                    "%Y-%m-%d %H:%M:%S")
            duration_info = {}
            duration_info["tabid"] = duration_info["startStamp"] = mktime(start.timetuple())
            duration_info["startTime"] = start.strftime("%H:%M")
            duration_info["endTime"] = end.strftime("%H:%M")
            duration_info["endStamp"] = mktime(end.timetuple())

            if now_stamp >= duration_info["startStamp"]:  # 已经开始了
                now_start = duration["start"]  # 保存刚刚开始信息
                now_start_tabid = duration_info["tabid"]  # 保存刚刚开始信息
                duration_info["started"] = True
            elif now_stamp < duration_info["startStamp"]:  # 即将开始
                soon_start_stamp_list.append(duration_info["startStamp"])
                duration_info["started"] = False

            duration_list.append(duration_info)

        return {"duration_list":duration_list,
                "now_start": now_start,
                "now_start_tabid": now_start_tabid,
                "soon_start_stamp_list": soon_start_stamp_list}

    def post(self):
        """获取限时抢购某个阶段的商品信息列表"""
        now_time = self.get_argument("limitSaleId", None)
        try:
            now_start = datetime.fromtimestamp(float(now_time))
        except:
            now_start = None
        if not now_start:
            self.data["status"] = "success"
            self.write(self.data)
            return

        now_stamp = mktime(datetime.now().timetuple())
        if now_stamp < float(now_time):
            limited_type = "soon"
            self.data["saleStarted"] = False
        else:
            limited_type = "started"
            self.data["saleStarted"] = True

        limited_goods = goods_model.HomeLimitedGoods.list_goods_in_duration(now_start)
        goods_list = goods_model.list_goods_info(limited_goods, limited_type)
        self.data["status"] = "success"
        self.data["goodsList"] = goods_list
        self.write(self.data)

urls = [
    (r"/adv/(.*?)/?", WwwAdvertiseMentHanlder),
    (r"/activities/(.*?)/?", WwwActivityMentHanlder),
    (r"/flash_sale/?", WwwLimitBuyHandler),
]

#!/usr/bin/env python
# coding:utf-8

import uuid
from datetime import datetime

from meihuishuo.libs.decorators import www_authenticated
from meihuishuo.libs.handlers import WwwBaseHandler
from meihuishuo.libs.pagination import Paginator
from meihuishuo.models import goods_model
from meihuishuo.models.goods_model import Goods, CurrencyType, \
    Effect, GoodsImg, Country, GoodspecificationType, \
    Comment, HomeLimitedGoods, Collection, ScoreOpinion
from meihuishuo.models.home_model import Shop


class WwwGoodsBaseHandler(WwwBaseHandler):
    """商品详情基类
    """
    def _get_comments(self, goods_id, start=1, page_count=15):
        """获取商品评论

        :param goods_id:　商品ID
        :param start: 当前页
        :param page_count:　每页评论数目
        :return:
        """
        comments_result = []
        comments, members = Comment.get_goods_comment_by_id(goods_id)
        if not comments:
            return comments_result

        for comment in comments[(start-1)*page_count:(start-1)*page_count+page_count]:
            detail = {}
            detail["is_essence"] = comment.is_essence
            detail["content"] = comment.content
            detail["photos"] = []
            photo_ids = comment.photo_ids
            if photo_ids:
                photo_ids = photo_ids.split(",")
            else:
                photo_ids = []
            for photo_id in photo_ids:
                detail["photos"].append(self.build_photo_url(photo_id, "thumb"))
            for member in members:
                if member.member_id == comment.create_person:
                    detail["member_name"] = member.member_name
                    if member.member_avatar:
                        detail["member_avatar"] = self.build_photo_url(member.member_avatar)
                    else:
                        detail["member_avatar"] = "/images/user-default.jpg"
                    break
            else:
                detail["member_name"] = None
                detail["member_avatar"] = "/images/user-default.jpg"
            detail["title"] = comment.title
            detail["score"] = comment.score
            detail["create_time"] = str(comment.create_time)
            comments_result.append(detail)

        return comments_result

    def _get_goods_score(self, goods_id):
        """获取商品综合评分

        :param goods_id:　需要查询的商品ID
        :return: 评分
        """
        score_lists = ScoreOpinion.get_goods_score(goods_id)
        score = "5.0"
        for score_list in score_lists:
            if score_list.score:
                score = str(round(score_list.score, 1))
                if len(score) == 1:
                    score = score+".0"

        return score


class WWWGoodsDetail(WwwGoodsBaseHandler):
    def get(self, goods_id):

        category_list = self.get_category()
        current_user = self.current_user
        if not goods_id:
            self.send_error(404)
            return

        if current_user and current_user.is_staff:
            goods = Goods.get_goods_by_goods_id(goods_id, goods_status="all_status")
        else:
            goods = Goods.get_goods_by_goods_id(goods_id)
        if not goods:
            self.send_error(404)
            return
        try:
            member_id = current_user.member_id
        except:
            member_id = None
        seach_dict = {"goods_id":goods_id, "member_id":member_id}
        goods_detail = goods_model.find_goods_detail(seach_dict)

        if not goods_detail:
            self.send_error(404)
            return

        self.data["message"] = ""
        if not goods_detail["is_favorite"] or not member_id:
            goods_detail["is_favorite"] = "0"

        # if not goods_detail["high_score_rate"]:
        #     goods_detail["high_score_rate"] = "100%"

        limited_goods = HomeLimitedGoods.load_limited_goods_by_goods_id(goods_id)
        if limited_goods:
            if int(goods_detail["stock_count"]) > limited_goods.goods_left_count:
                goods_detail["stock_count"] = limited_goods.goods_left_count

            if goods_detail["stock_count"] < 1:
                goods_detail["is_sold_out"] = 1
            else:
                goods_detail["is_sold_out"] = 0
        else:
            if int(goods_detail["stock_count"]) < 1:
                goods_detail["is_sold_out"] = 1
            else:
                goods_detail["is_sold_out"] = 0

        if not goods_detail["price"]:
            goods_detail["price"] = 0

        goods_detail["discount"] = str(round(float(goods_detail["price"])/\
                                       float(goods_detail["domestic_price"])*10, 1))

        symbol = CurrencyType.get_symbol(goods.foreign_type)
        good_effects = Effect.find_effect_by_id(goods_id)
        brand = Shop.find_shop_img_by_shop_id(goods.shop_id)
        specifications_type_name = GoodspecificationType.get_goodspecification_type_name(goods.specifications_type)
        country = None
        if brand:
            country = Country.get_country(brand.country_id)
            goods_detail["country"] = country.country_cn_name + \
                " / " + country.country_en_name
        else:
            goods_detail["country"] = ""

        if country:
            goods_detail["country_img_url"] = self.build_country_img_url(country.country_id)
        else:
            goods_detail["country_img_url"] = ""

        effect_value = ""
        if good_effects:
            for good_effect in good_effects:
                effect_value = effect_value + " " + \
                    good_effect.effect_title
            effect_value = effect_value[1: len(effect_value)]
        goods_detail["effect"] = effect_value

        goods_img = GoodsImg.find_goods_img_by_id(goods_id)
        img_list = []
        for img in goods_img:
            img_url = self.build_photo_url(img.img_view, "hd", pic_type="goods", cdn=True)
            img_list.append(img_url)
        goods_detail["img_urls"] = img_list

        carousel_imgs = GoodsImg.list_goods_img(goods_id, 1)
        carousel_img_list = []
        for img in carousel_imgs:
            img_url = self.build_photo_url(img.img_view, "thumb", pic_type="goods", cdn=True)
            carousel_img_list.append(img_url)
        goods_detail["carousel_imgs"] = carousel_img_list

        goods_detail["applicable"] = goods.applicable
        goods_detail['shelf_life'] = goods.shelf_life

        if specifications_type_name:
            goods_detail["specifications"] = goods.specifications.encode("utf8") + \
                                             specifications_type_name.encode("utf8")
        else:
            goods_detail["specifications"] = goods.specifications.encode("utf8")
        if brand:
            if brand.brand_cn_name != brand.brand_en_name:
                goods_detail["brand"] = brand.brand_cn_name + "/" + \
                    brand.brand_en_name
            else:
                goods_detail["brand"] = brand.brand_cn_name
        else:
            goods_detail["brand"] = ""

        if goods_detail["carousel_imgs"]:
            goods_detail["img_enlarg"] = goods_detail["carousel_imgs"][0].replace("thumb", "title")
        else:
            goods_detail["img_enlarg"] = self.build_photo_url(goods_detail["share_image"], "title", pic_type="goods", cdn=True)
        goods_detail["image"] = self.build_photo_url(goods_detail["share_image"], "thumb", pic_type="goods", cdn=True)
        comment_len = Comment.get_comment_count_by_goods_id(goods.goods_id)
        goods_detail["comments"] = self._get_comments(goods.goods_id)
        goods_detail["new_buyer"] = True if goods.sale_type == "new_buyer" else False

        goods_detail["score"] = str(int(float(goods.score)*20))+"%" if goods.score else "100%"

        # 内购相关
        goods_detail["is_not_avail"] = 0
        staff_goods = goods_model.StaffGoods.load_goods_by_id(goods_id, online=True)
        if staff_goods and current_user and current_user.is_staff:
            if goods.stock < staff_goods.stock:
                goods_detail["stock_count"] = goods.stock
            else:
                goods_detail["stock_count"] = staff_goods.stock
            if staff_goods.status != "1":
                goods_detail["is_not_avail"] = 1
        else:
            if goods.status != "1":
                goods_detail["is_not_avail"] = 1

        # 分页实现
        paginator = Paginator(comment_len, 15)
        page = paginator.page(1)
        pages = paginator.calculate_display_pages(1)
        page_num = paginator.total_pages
        less_than_certain_size = paginator.check_less_than_certain_size()
        page_args = {"page": page, "pages": pages, "page_num":page_num, "less_than_certain_size": less_than_certain_size}

        self._render(goods_detail, comment_len, staff_goods, category_list, page_args)

    def _render(self, goods_detail=None, comment_len=None, staff_goods=None, category_list=[], args={}):
        self.render("www/w_goods_detail.html",
                    goods_detail=goods_detail,
                    comment_len=comment_len,
                    category_list=category_list,
                    page=args["page"], page_num=args["page_num"],
                    pages=args["pages"],
                    less_than_certain_size=args["less_than_certain_size"],
                    id=None, parent=None, staff_goods=staff_goods)


class WwwCollectionHandler(WwwBaseHandler):
    def handle_collection(self, action, collection_info):
        member_id = self.current_user.member_id
        if action == "1":  # add collection
            # 删除已有的商品数据
            Collection.delete_collection(member_id,
                                         collection_info["goods_id"])
            collection = Collection()
            collection.member_id = member_id
            collection.collection_type = action
            collection.related_type = collection_info["related_type"]
            collection.related_id = collection_info["goods_id"]
            collection.collection_id = str(uuid.uuid4())
            collection.create_time = datetime.now()
            collection.save(force_insert=True)
        elif action == "2":  # cancel collection
            Collection.delete_collection(member_id,
                                         collection_info["goods_id"])


class WwwCollectionAddHandler(WwwCollectionHandler):
    @www_authenticated
    def post(self):

        collection_info = {}
        collection_info["goods_id"] = self.get_argument("goods_id", None)
        collection_info["related_type"] = self.get_argument("related_type", None)

        if not collection_info["goods_id"] and \
           not collection_info["related_type"]:
            self.data["status"] = "error"
            self.data["message"] = "收藏失败"
            self.write(self.data)
            return

        self.handle_collection(action="1", collection_info=collection_info)
        self.data["status"] = "success"
        self.write(self.data)


class WwwCollectionDeleteHandler(WwwCollectionHandler):
    @www_authenticated
    def post(self):

        collection_info = {}
        collection_info["goods_id"] = self.get_argument("goods_id", None)
        collection_info["related_type"] = self.get_argument("related_type", None)

        if not collection_info["goods_id"] and \
           not collection_info["related_type"]:
            self.data["status"] = "error"
            self.data["message"] = "收藏失败"
            self.write(self.data)
            return

        self.handle_collection(action="2", collection_info=collection_info)
        self.data["status"] = "success"
        self.write(self.data)


class WwwCommentHandler(WwwGoodsBaseHandler):
    """商品评论的分页获取
    """
    def get(self):
        current_page_num = self.get_argument("curentPageNum", 1)
        page_size = self.get_argument("pageSize", 15)
        goods_id = self.get_argument("goods_id", None)
        if not goods_id:
            self.write(self.data)
            return

        self.data["total"] = Comment.get_comment_count_by_goods_id(goods_id)
        self.data["current_page_num"] = current_page_num
        self.data["page_size"] = page_size
        # 页数
        self.data["page_count"] = self.data["total"]/int(page_size) + \
                                  (1 if self.data["total"]%int(page_size) else 0)

        # 获取评论列表
        self.data["comments"] = self._get_comments(goods_id=goods_id,
                                                   start=int(current_page_num),
                                                   page_count=int(page_size))

        self.data["status"] = "success"
        self.write(self.data)


urls = [
    (r"/goods/([a-z0-9-]+)/?", WWWGoodsDetail),
    (r"/collection/add/?", WwwCollectionAddHandler),
    (r"/collection/delete/?", WwwCollectionDeleteHandler),
    (r"/comments/?", WwwCommentHandler),
]

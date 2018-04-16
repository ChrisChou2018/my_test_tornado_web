# coding:utf-8

import random

from meihuishuo.libs.handlers import JsWwwBaseHandler
from meihuishuo.models.goods_model import Goods, GoodsType, Brand, BrandType
from meihuishuo.models.shop_model import Type

class RecommendHandler(JsWwwBaseHandler):
    """推荐商品
    """
    def get(self):
        goods_id = self.get_argument("goods_id", "")
        limit_count = self.get_argument("limit_count", "5")
        if limit_count.isdigit():
            limit_count = int(limit_count)
        else:
            limit_count = 5
        recommend_type = self.get_argument("recommend_type", "")

        if not goods_id or not recommend_type:
            self.write(self.data)

        goods_ids = []
        if recommend_type == "brand":
            # 得到品牌一样的产品
            goods = Goods.get_goods_by_goods_id(goods_id)
            goods_ids = Goods.get_goods_id_by_shop_id(goods.shop_id)
        elif recommend_type == "type":
            # 得到type一样的产品
            goods_type_ids = []
            # 得到所有的 type id
            goods_types = GoodsType.get_goods_type_by_goods_id(goods_id)
            for item in goods_types:
                goods_type_ids.append(item.type_id)
            goods_types = GoodsType.list_goods_by_ids(goods_type_ids)
            for item in goods_types:
                goods_ids.append(item.goods_id)

        goods_ids.remove(goods_id)  # 删除该页面商品ID

        goods_list = []
        if goods_ids:
            goods_list = Goods.list_goods_by_ids(goods_ids, "normal")
        goods_result = []
        for goods in goods_list:
            goods_info = {}
            goods_info['goodsId'] = goods.goods_id
            goods_info["price"] = str(goods.current_price)
            goods_info["buy_count"] = goods.buy_count
            goods_info["title"] = goods.goods_title
            goods_info["img_url"] = self.build_photo_url(goods.img_view, pic_type="goods", cdn=True)
            goods_info["domestic_price"] = str(goods.domestic_price)
            goods_result.append(goods_info)
        random.shuffle(goods_result)  # 打乱顺序

        self.data["list"] =goods_result[:limit_count]
        self.data["totalCount"] = len(self.data["list"])
        self.data["result"] = "success"
        self.write(self.data)


urls = [
    (r"/getRecommendGoods", RecommendHandler)
]
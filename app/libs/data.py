#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

roles = ("editor", "operator", "admin")

# member_role = {
#     "admin":("admin", ),
#     "editor":("zmxu", )
# }

permission_dict = {
    "brand": {
        "look_brands", "look_brand_detail", "edit_brand", "delete_brand", "insert_brand"
    },
    "home": {
        "look_home_new_goods", "insert_home_goods", "delete_home_goods", "look_home_goods_detail",
        "edit_home_goods", "look_home_essence_goods", "look_home_advertisements", "look_advertisement_detail",
        "insert_advertisement", "edit_advertisement", "look_advertisement_goods", "insert_advertisement_goods",
        "look_cate_goods", "look_home_cates", "delete_home_goods"
    },
    "coupon": {
        "look_coupon_sets", "look_condition_coupon_sets", "insert_coupon_set", "insert_condition_coupon_set",
        "look_coupons", "edit_coupon_set", "edit_condition_coupon_set", "look_coupon_set_detail", "delete_coupon_set",
        "delete_coupon"
    },
    "limited": {
        "look_limited_goods", "edit_limited_goods", "insert_limited_goods", "delete_limited_goods",
        "look_limited_goods_detail"
    },
    "staff_goods": {
        "look_staff_goods", "edit_staff_goods", "insert_staff_goods", "delete_staff_goods",
        "look_staff_goods_detail", "update_staff_goods"
    },
    "orders": {
        "look_orders", "edit_logistic", "look_logistic", "look_order_detail", "order_shopping",
        "delete_logistic", "update_logistic", "insert_logistic"
    },
    "goods": {
        "look_goods", "insert_goods", "look_goods_detail", "edit_goods", "upload_goods_roll_img",
        "delete_goods_roll_img", "look_comments", "delete_comment", "look_comment_detail", "edit_comment",
        "insert_comment", "look_warehouse_goods", "look_goods_imgs", "look_goods_real_imgs", "edit_goods_warehouse",
        "delete_goods", "look_types", "delete_type", "look_type_detail", "insert_type", "edit_type",
        "update_goods_detail_imgs", "delete_goods_detail_img", "delete_effect", "look_effect_detail",
        "edit_effect", "insert_effect", "look_specification", "delete_specification", "specification_detail",
        "edit_specification", "insert_specification", "look_specifications", "excel", "comment_member_manager",
        "comment_manager"
    },
    "user_manager": {
        "look_users", "delete_user", "insert_user", "change_user_password", "edit_user"
    },
    "version": {
        "look_versions", "insert_version", "version"
    },
    "warehouse": {
        "look_warehouses", "delete_warehouse", "warehouse_detail", "look_purchase_orders",
        "delete_purchase_order", "purchase_order_detail", "insert_purchase_goods",
        "insert_purchase_order_goods", "delete_purchase_goods", "update_purchase_order_goods"
    },
    "category": {
        "category_effects", "category_brand", "add_category_effect", "add_category_brand",
        "delete_category", "category_detail", "update_category", "category_other", "add_category_other",
        "update_category_other", "category_other_list", "add_category_other_item"
    },
    "other": {},
    "activity": {"activity"},
    "feedback": {"feedback"},
    "member": {"member"},
    "metadata": {"metadata"},
    "articles": {"articles"},
    "push": {"push"},
    "questionnaire": {"questionnaire"},
}

role_permission = {
    "admin":(
        "brand", "home", "coupon", "limited", "orders", "goods",
        "user_manager", "version", "warehouse", "category", "other",
        "activity", "feedback", "member", "metadata", "articles", "push",
        "questionnaire", "staff_goods"
    ),
    "operator":(
        "brand", "home", "coupon", "limited", "orders", "goods",
        "warehouse", "category", "other", "articles", "staff_goods"
    ),
    "editor":(
        "goods", "articles"
    ),
}


skintest_suites = [
    {"id": "suite_1", "title": "干性/油性测试"},
    {"id": "suite_2", "title": "敏感/耐受性测试"},
    {"id": "suite_3", "title": "色素/非色素性测试"},
    {"id": "suite_4", "title": "易皱纹/紧致测试"},
]

order_status_titles = {
    "1": "待付款", "2": "待发货", "3": "待收货", "4": "待评价",
    "10": "交易关闭", "11": "未付款,未成团", "12": "已付款,未成团",
    "13": "已成团,待发货", "14": "已成团,待收货", "15": "已成团,待评价",
    "16": "未成团,已退款", "17": "未成团,待退款", "99": "订单已删除"
}

shop_names = [
    {"id": "xymt", "name": u"新氧美淘"},
    {"id": "bl", "name": u"百联"},
    {"id": "ml15yf_ml13y", "name": u"美丽15姨夫-美丽13姨"},
    {"id": "yzgj", "name": u"优妆国际"},
    {"id": "ngw", "name": u"内购网"},
    {"id": "heynaturehwqjd", "name": u"heynature海外旗舰店"},
    {"id": "higo_mhs", "name": u"HIGO-美会说"},
    {"id": "mayfunhqmzd", "name": u"MAYFUN环球美妆店"},
    {"id": "jd_heynaturehwqjd", "name": u"京东-Heynature（韩妮采）海外旗舰店"},
    {"id": "ybsyzhwg", "name": u"优贝施药妆海外购"},
    {"id": "bjzzyxkjyxgs", "name": u"北京众智易讯科技有限公司"},
    {"id": "nhkjggjsh", "name": u"南航跨境购国际生活"},
    {"id": "xnnmonica", "name": u"小腻腻niniMONICA"},
    {"id": "wtbp", "name": u"屋托邦派"},
    {"id": "wd_mhs", "name": u"微店-美会说"},
    {"id": "sgshlm", "name": u"手工生活联盟"},
    {"id": "rxlp", "name": u"日欣良品"},
    {"id": "yzyzupskin", "name": u"有赞优妆UPSKIN"},
    {"id": "yjxpmml", "name": u"有间小铺卖美丽"},
    {"id": "szsbnyydzswyxgs", "name": u"深圳市百年远洋电子商务有限公司"},
    {"id": "mhsapp", "name": u"美会说APP"},
    {"id": "mhs", "name": u"美会说"},
    {"id": "mfj", "name": u"美肤家"},
    {"id": "mhshzpqqg", "name": u"美会说化妆品全球购"},
    {"id": "mhshwzyd", "name": u"美会说海外专营店"},
    {"id": "mhshwqqg", "name": u"美会说海外全球购"},
    {"id": "mhshwhzpzyd", "name": u"美会说海外化妆品专营店"},
    {"id": "hzcp", "name": u"韩妆潮品"},
    {"id": "hnchwqjd", "name": u"韩妮采海外旗舰店"},
]

warehouses_name = ["分销仓---美会说"]

assets_dict = {}


provinces = {
    "neimenggu": u"内蒙古",
    "hainan": u"海南",
    "jiangsu": u"江苏",
    "xizang": u"西藏",
    "shandong": u"山东",
    "xinjiang": u"新疆",
    "shanxi": u"山西",
    "guangxi": u"广西",
    "shanghai": u"上海",
    "yunnan": u"云南",
    "jiangxi": u"江西",
    "ningxia": u"宁夏",
    "hebei": u"河北",
    "guangdong": u"广东",
    "heilongjiang": u"黑龙江",
    "guizhou": u"贵州",
    "fujian": u"福建",
    "qinghai": u"青海",
    "tianjin": u"天津",
    "hunan": u"湖南",
    "taiwang": u"台湾",
    "jilin": u"吉林",
    "sichuang": u"四川",
    "anhui": u"安徽",
    "gansu": u"甘肃",
    "beijing": u"北京",
    "hubei": u"湖北",
    "aomen": u"澳门",
    "liaoning": u"辽宁",
    "chongqing": u"重庆",
    "zhejiang": u"浙江",
    "henan": u"河南",
    "xianggan": u"香港",
    "shan_xi": u"陕西"
}


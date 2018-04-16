#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib
import unittest
import tornado.testing
import tornado.httpclient

import meihuishuo.handlers.api.api_home as handler_api_home

from meihuishuo.tests.test_base import BaseHTTPTestCase


class CommonCheck(object):
    pass


class ApiAppHomeHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppHomeHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppHomeHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_home(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output: [
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/home/f69f91de-b426-4c02-b036-05b427bf99da.JPG',
            u'RelatedId': u'5bb1655b-18ce-400e-8d03-81d64af5b70a', u'IfMiddlePage': u'0', u'CommodityText': None}
            ]
        '''
        response = self.fetch(
            "/v1/ads/home", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_app_home(json_data)

    def _check_app_home(self, json_data):
        if json_data:
            print "AppHome:", json_data


class ApiAppActivityListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppActivityListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppActivityListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_activity_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:[
            {u'LogoImg': u'http://123.56.109.37:8080/beautalk/localfile/groupon/0191a01e-1f2d-47f6-9d84-acc4b48b1a5e.JPG',
            u'IfMiddlePage': u'1', u'ActivityDate': u'10天17时40分', u'CommodityText':
            u'1周三特卖！wnw持久不脱色口红，绽放美唇诱惑，让他一见倾心！', u'Content': u'全场5.8折起',
            u'ActivityId': u'6034360d-d158-4960-aca9-99605dcbacdc', u'ShopTitle': u'全场',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/groupon/2eba05a1-f2b8-44dd-8cf5-29307be929d4.JPG',
            u'FormetDate': u'<font color=black>10</font>天<font color=black>17</font>时<font color=black>40</font>分'},
            {u'LogoImg': u'http://123.56.109.37:8080/beautalk/localfile/groupon/0f91e7f9-b0a0-4437-906e-5c99ec683efd.JPG',
            u'IfMiddlePage': u'0', u'ActivityDate': u'10天11时45分', u'CommodityText': u'123123123', u'Content': u'全场3折起',
            u'ActivityId': u'b2c4a54c-5fea-4175-a9d5-8079c94ccd9d', u'ShopTitle': u'全场',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/groupon/0b308625-911a-4957-bb71-cca371acd10f.JPEG',
            u'FormetDate': u'<font color=black>10</font>天<font color=black>11</font>时<font color=black>45</font>分'}
            ]
        '''
        response = self.fetch(
            "/v1/activities/", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_app_activity_list(json_data)

    def _check_app_activity_list(self, json_data):
        if json_data:
            print "AppActivityList:", json_data


class ApiFindGrouponMiddleListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindGrouponMiddleListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindGrouponMiddleListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_find_groupon_middle_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:
        '''
        response = self.fetch(
            "/v1/gpromos/mpage_pics", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_groupon_middle_list(json_data)

    def _check_find_groupon_middle_list(self, json_data):
        if json_data:
            print "ApiFindGrouponMiddleList:", json_data


class ApiAppGrounpGoodsListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppGrounpGoodsListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppGrounpGoodsListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_grounp_goods_list(self):
        # request_body = urllib.urlencode()
        '''
        Input: ?search=123123123&GrouponId=b2c4a54c-5fea-4175-a9d5-8079c94ccd9d&OrderName=host&PageNum=1&OrderType=DESC
        Output:[
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'ForeignPrice': u'₩17841', u'Title': u'芭妮兰致柔卸妆膏100ml', u'GoodsId': u'2483093f-b8be-4b0b-8514-7645b43c982a',
            u'Price': u'￥78.0', u'OtherPrice': u'海外官网价：₩18000 大陆官网价：￥198', u'BuyCount': u'641', u'Alert': u'0',
            u'CountryName': u'Korea 韩国原装', u'Discount': u'3.9', u'ActivityStock': u'10', u'RestTime': u'还剩10天11小时18分钟',
            u'Abbreviation': u'芭妮兰致柔卸妆膏100ml', u'ImgView':
            u'http://123.56.109.37:8080/beautalk/localfile/2483093f-b8be-4b0b-8514-7645b43c982a/goods/41f2fdda-7ebf-4ec3-9e80-284ffb8ab50d.JPG',
            u'FormetDate': u'还剩10天11小时18分钟', u'DomesticPrice': u'198', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'ForeignPrice': u'$4.5', u'Title': u'wet n wild whw持久不脱色口红968 3.3g', u'GoodsId': u'7dcce713-5280-4929-968d-02bcfb18de84',
            u'Price': u'￥39.0', u'OtherPrice': u'海外官网价：$7.7 大陆官网价：￥48', u'BuyCount': u'146', u'Alert': u'0', u'CountryName':
            u'U.S.A 美国原装', u'Discount': u'8.1', u'ActivityStock': u'10', u'RestTime': u'还剩10天11小时18分钟', u'Abbreviation':
            u'wet n wild whw持久不脱色口红3.3g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/7dcce713-5280-4929-968d-02bcfb18de84/goods/5bc3e163-aeed-423e-8445-2796ef1fe485.JPG',
            u'FormetDate': u'还剩10天11小时18分钟', u'DomesticPrice': u'48', u'Stock': u'10'}]
        '''
        '''
        Input: ?search=&GrouponId=b2c4a54c-5fea-4175-a9d5-8079c94ccd9d&OrderName=host&PageNum=1&OrderType=DESC
        Output:[
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'ForeignPrice': u'₩17841', u'Title': u'芭妮兰致柔卸妆膏100ml', u'GoodsId': u'2483093f-b8be-4b0b-8514-7645b43c982a',
            u'Price': u'￥78.0', u'OtherPrice': u'海外官网价：₩18000 大陆官网价：￥198', u'BuyCount': u'641', u'Alert': u'0',
            u'CountryName': u'Korea 韩国原装', u'Discount': u'3.9', u'ActivityStock': u'10', u'RestTime': u'还剩10天11小时18分钟',
            u'Abbreviation': u'芭妮兰致柔卸妆膏100ml', u'ImgView':
            u'http://123.56.109.37:8080/beautalk/localfile/2483093f-b8be-4b0b-8514-7645b43c982a/goods/41f2fdda-7ebf-4ec3-9e80-284ffb8ab50d.JPG',
            u'FormetDate': u'还剩10天11小时18分钟', u'DomesticPrice': u'198', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'ForeignPrice': u'$4.5', u'Title': u'wet n wild whw持久不脱色口红968 3.3g', u'GoodsId': u'7dcce713-5280-4929-968d-02bcfb18de84',
            u'Price': u'￥39.0', u'OtherPrice': u'海外官网价：$7.7 大陆官网价：￥48', u'BuyCount': u'146', u'Alert': u'0', u'CountryName':
            u'U.S.A 美国原装', u'Discount': u'8.1', u'ActivityStock': u'10', u'RestTime': u'还剩10天11小时18分钟', u'Abbreviation':
            u'wet n wild whw持久不脱色口红3.3g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/7dcce713-5280-4929-968d-02bcfb18de84/goods/5bc3e163-aeed-423e-8445-2796ef1fe485.JPG',
            u'FormetDate': u'还剩10天11小时18分钟', u'DomesticPrice': u'48', u'Stock': u'10'}]
        '''
        '''
        Input: ?search=&GrouponId=&OrderName=host&PageNum=1&OrderType=DESC
        Output:[
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'芭妮兰致柔卸妆膏100ml', u'GoodsId': u'2483093f-b8be-4b0b-8514-7645b43c982a', u'Price': u'￥158.0',
            u'OtherPrice': u'海外官网价：₩18000 大陆官网价：￥198', u'BuyCount': u'641', u'Alert': u'0', u'CountryName':
            u'Korea 韩国原装', u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'芭妮兰致柔卸妆膏100ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/2483093f-b8be-4b0b-8514-7645b43c982a/goods/41f2fdda-7ebf-4ec3-9e80-284ffb8ab50d.JPG',
            u'ForeignPrice': u'₩17841', u'DomesticPrice': u'198', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'菲诗小铺清爽控油金盏花爽肤水150ml', u'GoodsId': u'8467373b-a52f-424a-9aff-2979e002c586', u'Price': u'￥99.0',
            u'OtherPrice': u'海外官网价：₩6900 大陆官网价：￥134', u'BuyCount': u'624', u'Alert': u'0', u'CountryName':
            u'Korea 韩国原装', u'Discount': u'', u'ActivityStock': u'1', u'Abbreviation': u'菲诗小铺清爽控油金盏花爽肤水150ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/8467373b-a52f-424a-9aff-2979e002c586/goods/f14f3218-7131-4f79-a341-4a47a87226cf.JPG',
            u'ForeignPrice': u'₩12358', u'DomesticPrice': u'134', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'菲诗小铺大米植物妆前隔离霜绿色40ml', u'GoodsId': u'9db265fc-817a-454d-b583-ab95a1bab842', u'Price': u'￥49.0',
            u'OtherPrice': u'海外官网价：₩3300 大陆官网价：￥59', u'BuyCount': u'573', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'菲诗小铺大米植物妆前隔离霜绿色40ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/9db265fc-817a-454d-b583-ab95a1bab842/goods/5049d42b-f62f-4a2f-93a4-aae5d50f87f6.JPG',
            u'ForeignPrice': u'₩5634', u'DomesticPrice': u'59', u'Stock': u'10'}, {u'CountryImg':
            u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg', u'Title':
            u'PhytoTree 芝士奶酪护手霜50g', u'GoodsId': u'2ec784c0-70d1-45c9-9722-cd27c03932a7', u'Price': u'￥45.0', u'OtherPrice': u'海外官网价：₩12469 大陆官网价：￥69',
            u'BuyCount': u'429', u'Alert': u'0', u'CountryName': u'Korea 韩国原装', u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation':
            u'PhytoTree芝士奶酪护手霜50g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/2ec784c0-70d1-45c9-9722-cd27c03932a7/goods/43e2476a-0d11-47d0-a713-f2c9788f5609.JPG',
            u'ForeignPrice': u'₩6867', u'DomesticPrice': u'69', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'可莱丝NMF针剂水库面膜25ml*10', u'GoodsId': u'2480605f-cb5f-47f5-8dff-869f9a0d6a0a', u'Price': u'￥128.0',
            u'OtherPrice': u'海外官网价：₩33000 大陆官网价：￥216', u'BuyCount': u'654', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'可莱丝NMF针剂水库面膜25ml*10',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/2480605f-cb5f-47f5-8dff-869f9a0d6a0a/goods/269d089b-8f8a-4885-8368-3cea60447fca.JPG',
            u'ForeignPrice': u'₩19489', u'DomesticPrice': u'216', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg', u'Title':
            u'3CE猪油膏打底霜隐形毛孔25g', u'GoodsId': u'acaa569e-8942-4a34-8d9e-33aca1c79ac4', u'Price': u'￥89.0', u'OtherPrice':
            u'海外官网价：₩13000 大陆官网价：￥93.28', u'BuyCount': u'935', u'Alert': u'0', u'CountryName': u'Korea 韩国原装', u'Discount': u'',
            u'ActivityStock': u'0', u'Abbreviation': u'3CE猪油膏打底霜隐形毛孔25g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/acaa569e-8942-4a34-8d9e-33aca1c79ac4/goods/fdd1bdfc-4dd5-4bf3-b4f6-0064bd574ade.JPG',
            u'ForeignPrice': u'₩16015', u'DomesticPrice': u'93.28', u'Stock': u'0'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'3CE LIP COLOR保湿润唇膏402 4g', u'GoodsId': u'549866b0-5fdc-461f-8dc2-8b9b4ef6d104', u'Price': u'￥109.0',
            u'OtherPrice': u'海外官网价：₩17900 大陆官网价：￥124.38', u'BuyCount': u'631', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'3CE LIP COLOR保湿润唇膏402 4g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/549866b0-5fdc-461f-8dc2-8b9b4ef6d104/goods/ab9face3-314f-4cf7-8ab5-3ca776db2d43.JPG',
            u'ForeignPrice': u'₩17796', u'DomesticPrice': u'124.38', u'Stock': u'1'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'九朵云保湿美白祛斑霜50ml', u'GoodsId': u'8b27e8ea-46d1-483d-b336-3617384e2fa7', u'Price': u'￥138.0',
            u'OtherPrice': u'海外官网价：₩59000 大陆官网价：￥168', u'BuyCount': u'697', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'九朵云保湿美白祛斑霜50ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/8b27e8ea-46d1-483d-b336-3617384e2fa7/goods/2f37843b-76f0-4264-86af-b1032814dc93.JPG',
            u'ForeignPrice': u'₩17796', u'DomesticPrice': u'168', u'Stock': u'52'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'九朵云奇迹马油精华水120ml', u'GoodsId': u'a8a23358-b8f3-4e96-8c85-5c0d825ccc09', u'Price': u'￥128.0',
            u'OtherPrice': u'海外官网价：₩66499 大陆官网价：￥369', u'BuyCount': u'526', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'九朵云奇迹马油精华水120ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/a8a23358-b8f3-4e96-8c85-5c0d825ccc09/goods/cadfc6a2-c519-4f3b-8352-31e663ab1bbc.JPG',
            u'ForeignPrice': u'₩21265', u'DomesticPrice': u'369', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'伊思 蜗牛精华水乳套装 140ml*2', u'GoodsId': u'caa5dbb9-2e24-466b-8867-bffafae1a5f0', u'Price': u'￥416.0',
            u'OtherPrice': u'海外官网价：₩76000 大陆官网价：￥520', u'BuyCount': u'543', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'神奇蜗牛水乳套装',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/caa5dbb9-2e24-466b-8867-bffafae1a5f0/goods/0ac02763-dadb-4266-9bf5-a255663537be.JPG',
            u'ForeignPrice': u'₩71269', u'DomesticPrice': u'520', u'Stock': u'10'}
            ]
        '''
        '''
        Input: ?search=&GrouponId=&OrderName=host&PageNum=1&OrderType=DESC
        Output:[
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'芭妮兰致柔卸妆膏100ml', u'GoodsId': u'2483093f-b8be-4b0b-8514-7645b43c982a', u'Price': u'￥158.0',
            u'OtherPrice': u'海外官网价：₩18000 大陆官网价：￥198', u'BuyCount': u'641', u'Alert': u'0', u'CountryName':
            u'Korea 韩国原装', u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'芭妮兰致柔卸妆膏100ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/2483093f-b8be-4b0b-8514-7645b43c982a/goods/41f2fdda-7ebf-4ec3-9e80-284ffb8ab50d.JPG',
            u'ForeignPrice': u'₩17841', u'DomesticPrice': u'198', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'菲诗小铺清爽控油金盏花爽肤水150ml', u'GoodsId': u'8467373b-a52f-424a-9aff-2979e002c586', u'Price': u'￥99.0',
            u'OtherPrice': u'海外官网价：₩6900 大陆官网价：￥134', u'BuyCount': u'624', u'Alert': u'0', u'CountryName':
            u'Korea 韩国原装', u'Discount': u'', u'ActivityStock': u'1', u'Abbreviation': u'菲诗小铺清爽控油金盏花爽肤水150ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/8467373b-a52f-424a-9aff-2979e002c586/goods/f14f3218-7131-4f79-a341-4a47a87226cf.JPG',
            u'ForeignPrice': u'₩12358', u'DomesticPrice': u'134', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'菲诗小铺大米植物妆前隔离霜绿色40ml', u'GoodsId': u'9db265fc-817a-454d-b583-ab95a1bab842', u'Price': u'￥49.0',
            u'OtherPrice': u'海外官网价：₩3300 大陆官网价：￥59', u'BuyCount': u'573', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'菲诗小铺大米植物妆前隔离霜绿色40ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/9db265fc-817a-454d-b583-ab95a1bab842/goods/5049d42b-f62f-4a2f-93a4-aae5d50f87f6.JPG',
            u'ForeignPrice': u'₩5634', u'DomesticPrice': u'59', u'Stock': u'10'}, {u'CountryImg':
            u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg', u'Title':
            u'PhytoTree 芝士奶酪护手霜50g', u'GoodsId': u'2ec784c0-70d1-45c9-9722-cd27c03932a7', u'Price': u'￥45.0', u'OtherPrice': u'海外官网价：₩12469 大陆官网价：￥69',
            u'BuyCount': u'429', u'Alert': u'0', u'CountryName': u'Korea 韩国原装', u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation':
            u'PhytoTree芝士奶酪护手霜50g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/2ec784c0-70d1-45c9-9722-cd27c03932a7/goods/43e2476a-0d11-47d0-a713-f2c9788f5609.JPG',
            u'ForeignPrice': u'₩6867', u'DomesticPrice': u'69', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'可莱丝NMF针剂水库面膜25ml*10', u'GoodsId': u'2480605f-cb5f-47f5-8dff-869f9a0d6a0a', u'Price': u'￥128.0',
            u'OtherPrice': u'海外官网价：₩33000 大陆官网价：￥216', u'BuyCount': u'654', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'可莱丝NMF针剂水库面膜25ml*10',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/2480605f-cb5f-47f5-8dff-869f9a0d6a0a/goods/269d089b-8f8a-4885-8368-3cea60447fca.JPG',
            u'ForeignPrice': u'₩19489', u'DomesticPrice': u'216', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg', u'Title':
            u'3CE猪油膏打底霜隐形毛孔25g', u'GoodsId': u'acaa569e-8942-4a34-8d9e-33aca1c79ac4', u'Price': u'￥89.0', u'OtherPrice':
            u'海外官网价：₩13000 大陆官网价：￥93.28', u'BuyCount': u'935', u'Alert': u'0', u'CountryName': u'Korea 韩国原装', u'Discount': u'',
            u'ActivityStock': u'0', u'Abbreviation': u'3CE猪油膏打底霜隐形毛孔25g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/acaa569e-8942-4a34-8d9e-33aca1c79ac4/goods/fdd1bdfc-4dd5-4bf3-b4f6-0064bd574ade.JPG',
            u'ForeignPrice': u'₩16015', u'DomesticPrice': u'93.28', u'Stock': u'0'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'3CE LIP COLOR保湿润唇膏402 4g', u'GoodsId': u'549866b0-5fdc-461f-8dc2-8b9b4ef6d104', u'Price': u'￥109.0',
            u'OtherPrice': u'海外官网价：₩17900 大陆官网价：￥124.38', u'BuyCount': u'631', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'3CE LIP COLOR保湿润唇膏402 4g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/549866b0-5fdc-461f-8dc2-8b9b4ef6d104/goods/ab9face3-314f-4cf7-8ab5-3ca776db2d43.JPG',
            u'ForeignPrice': u'₩17796', u'DomesticPrice': u'124.38', u'Stock': u'1'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'九朵云保湿美白祛斑霜50ml', u'GoodsId': u'8b27e8ea-46d1-483d-b336-3617384e2fa7', u'Price': u'￥138.0',
            u'OtherPrice': u'海外官网价：₩59000 大陆官网价：￥168', u'BuyCount': u'697', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'九朵云保湿美白祛斑霜50ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/8b27e8ea-46d1-483d-b336-3617384e2fa7/goods/2f37843b-76f0-4264-86af-b1032814dc93.JPG',
            u'ForeignPrice': u'₩17796', u'DomesticPrice': u'168', u'Stock': u'52'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'九朵云奇迹马油精华水120ml', u'GoodsId': u'a8a23358-b8f3-4e96-8c85-5c0d825ccc09', u'Price': u'￥128.0',
            u'OtherPrice': u'海外官网价：₩66499 大陆官网价：￥369', u'BuyCount': u'526', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'九朵云奇迹马油精华水120ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/a8a23358-b8f3-4e96-8c85-5c0d825ccc09/goods/cadfc6a2-c519-4f3b-8352-31e663ab1bbc.JPG',
            u'ForeignPrice': u'₩21265', u'DomesticPrice': u'369', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/9d535e83-1c6c-8c05-08e5-8ac81ab5a739.jpeg',
            u'Title': u'伊思 蜗牛精华水乳套装 140ml*2', u'GoodsId': u'caa5dbb9-2e24-466b-8867-bffafae1a5f0', u'Price': u'￥416.0',
            u'OtherPrice': u'海外官网价：₩76000 大陆官网价：￥520', u'BuyCount': u'543', u'Alert': u'0', u'CountryName': u'Korea 韩国原装',
            u'Discount': u'', u'ActivityStock': u'10', u'Abbreviation': u'神奇蜗牛水乳套装',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/caa5dbb9-2e24-466b-8867-bffafae1a5f0/goods/0ac02763-dadb-4266-9bf5-a255663537be.JPG',
            u'ForeignPrice': u'₩71269', u'DomesticPrice': u'520', u'Stock': u'10'}
            ]
        '''
        response = self.fetch(
            "/v1/gpromos/goods", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_app_grounp_goods_list(json_data)

    def _check_app_grounp_goods_list(self, json_data):
        if json_data:
            print "ApiAppGrounpGoodsList:", json_data


class ApiAppHomeGoodsListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppHomeGoodsListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppHomeGoodsListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_home_goods_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:
        '''
        response = self.fetch(
            "/v1/activities/goods", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_app_home_goods_list(json_data)

    def _check_app_home_goods_list(self, json_data):
        if json_data:
            print "ApiAppHomeGoodsList:", json_data


class ApiSearchListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiSearchListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiSearchListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_search_list(self):
        # request_body = urllib.urlencode()
        '''
        Input: ?search=Alpha%20&OrderName=host&TypeId=&PageNum=1&OrderType=DESC
        Output:[
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'Title': u'Alpha Hydrox果酸温和洁面乳177ml', u'Price': u'￥69.0', u'OtherPrice': u'海外官网价：$19.2 大陆官网价：￥120',
            u'BuyCount': u'431', u'Alert': u'0', u'CountryName': u'U.S.A 美国原装', u'Discount': u'',
            u'GoodsId': u'f617117f-c86d-4c25-8753-423672307d72', u'Abbreviation': u'Alpha Hydrox果酸温和洁面乳177ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/f617117f-c86d-4c25-8753-423672307d72/goods/a69ef641-90a8-454b-800a-2b887ce012bc.JPG',
            u'ForeignPrice': u'$11.1', u'DomesticPrice': u'120', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'Title': u'Alpha Hydrox经典果酸面霜56g', u'Price': u'￥78.0', u'OtherPrice': u'海外官网价：$19.2 大陆官网价：￥120',
            u'BuyCount': u'381', u'Alert': u'0', u'CountryName': u'U.S.A 美国原装', u'Discount': u'',
            u'GoodsId': u'd9db5707-acdf-4ff7-afc3-ba9502c9bf9a', u'Abbreviation': u'Alpha Hydrox经典果酸面霜56g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/d9db5707-acdf-4ff7-afc3-ba9502c9bf9a/goods/e959a8d6-b32b-4f40-84c6-c9c4e55a440e.JPG',
            u'ForeignPrice': u'$11.1', u'DomesticPrice': u'120', u'Stock': u'0'}
            ]
        '''
        '''
        Input: ?search=Alpha%20&OrderName=host&TypeId=&PageNum=1&OrderType=DESC
        Output:[
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'Title': u'Alpha Hydrox果酸温和洁面乳177ml', u'Price': u'￥69.0', u'OtherPrice': u'海外官网价：$19.2 大陆官网价：￥120',
            u'BuyCount': u'431', u'Alert': u'0', u'CountryName': u'U.S.A 美国原装', u'Discount': u'',
            u'GoodsId': u'f617117f-c86d-4c25-8753-423672307d72', u'Abbreviation': u'Alpha Hydrox果酸温和洁面乳177ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/f617117f-c86d-4c25-8753-423672307d72/goods/a69ef641-90a8-454b-800a-2b887ce012bc.JPG',
            u'ForeignPrice': u'$11.1', u'DomesticPrice': u'120', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'Title': u'Alpha Hydrox经典果酸面霜56g', u'Price': u'￥78.0', u'OtherPrice': u'海外官网价：$19.2 大陆官网价：￥120',
            u'BuyCount': u'381', u'Alert': u'0', u'CountryName': u'U.S.A 美国原装', u'Discount': u'',
            u'GoodsId': u'd9db5707-acdf-4ff7-afc3-ba9502c9bf9a', u'Abbreviation': u'Alpha Hydrox经典果酸面霜56g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/d9db5707-acdf-4ff7-afc3-ba9502c9bf9a/goods/e959a8d6-b32b-4f40-84c6-c9c4e55a440e.JPG',
            u'ForeignPrice': u'$11.1', u'DomesticPrice': u'120', u'Stock': u'0'}
            ...
            ]
        '''
        '''
        Input:
        Output:[
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'Title': u'Alpha Hydrox果酸温和洁面乳177ml', u'Price': u'￥69.0', u'OtherPrice': u'海外官网价：$19.2 大陆官网价：￥120',
            u'BuyCount': u'431', u'Alert': u'0', u'CountryName': u'U.S.A 美国原装', u'Discount': u'',
            u'GoodsId': u'f617117f-c86d-4c25-8753-423672307d72', u'Abbreviation': u'Alpha Hydrox果酸温和洁面乳177ml',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/f617117f-c86d-4c25-8753-423672307d72/goods/a69ef641-90a8-454b-800a-2b887ce012bc.JPG',
            u'ForeignPrice': u'$11.1', u'DomesticPrice': u'120', u'Stock': u'10'},
            {u'CountryImg': u'http://123.56.109.37:8080/beautalk/localfile/country/f862b581-333b-4000-9449-8f491a1f4f9a.JPG',
            u'Title': u'Alpha Hydrox经典果酸面霜56g', u'Price': u'￥78.0', u'OtherPrice': u'海外官网价：$19.2 大陆官网价：￥120',
            u'BuyCount': u'381', u'Alert': u'0', u'CountryName': u'U.S.A 美国原装', u'Discount': u'',
            u'GoodsId': u'd9db5707-acdf-4ff7-afc3-ba9502c9bf9a', u'Abbreviation': u'Alpha Hydrox经典果酸面霜56g',
            u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/d9db5707-acdf-4ff7-afc3-ba9502c9bf9a/goods/e959a8d6-b32b-4f40-84c6-c9c4e55a440e.JPG',
            u'ForeignPrice': u'$11.1', u'DomesticPrice': u'120', u'Stock': u'0'}
            ...
            ]
        '''
        '''
        Input:?search=hfjksdhfjksdh&OrderName=host&TypeId=&PageNum=1&OrderType=DESC
        Output:
        '''
        response = self.fetch(
            "/v1/search?search=hfjksdhfjksdh&OrderName=host&TypeId=&PageNum=1&OrderType=DESC", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_app_search_list(json_data)

    def _check_app_search_list(self, json_data):
        if json_data:
            print "ApiSearchList:", json_data



class ApiGetGoodsClassifyHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiGetGoodsClassifyHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiGetGoodsClassifyHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_get_goods_classify(self):
        # request_body = urllib.urlencode()
        '''
        Input:?TypeId=4a4cd77a-3316-4e83-b3d6-e20233d1b316&OrderType=DESC&OrderName=host&PageNum=1
        Output:[
            {u'TypeId': u'0a14b2b5-a4b4-48f7-a428-f2829e654324',
            u'list': [{u'TypeId': u'03ba13bb-7ca1-418f-87d2-f3a55904053d', u'Title': u'T区/特殊护理'},
                {u'TypeId': u'11dc2759-394f-4546-8a0c-3d22644cab97', u'Title': u'眼部护理'},
                {u'TypeId': u'171727e8-b6ad-4530-a024-52b312edd481', u'Title': u'洁面'},
                {u'TypeId': u'1cc37c7b-1a76-4be3-a1f3-818df09d0323', u'Title': u'精华'},
                {u'TypeId': u'a3e56d11-687d-4af8-b611-1add67d750fb', u'Title': u'面霜'},
                {u'TypeId': u'dac6eef7-c49d-4637-8c1d-052b439c5d46', u'Title': u'唇部护理'},
                {u'TypeId': u'dde8f3cb-c07c-43c8-93c0-06779d622462', u'Title': u'啫喱/凝露/凝胶'},
                {u'TypeId': u'e1486e88-1794-429d-af25-a1972f32e133', u'Title': u'化妆水/爽肤水'},
                {u'TypeId': u'efd47bdb-8bd5-4cc0-a865-7357fdfc3c36', u'Title': u'面膜'},
                {u'TypeId': u'f0cff16e-c5a2-40fe-8a73-f19c2c2a9df5', u'Title': u'乳液'},
                {u'TypeId': u'f43603f8-bd20-4c64-adf3-4f1203ba1875', u'Title': u'精油'}], u'Title': u'护肤'},
            {u'TypeId': u'1fe29d79-d37b-4a70-87c3-08e13169683f',
            u'list': [{u'TypeId': u'4e4bea3f-8a61-47a9-a786-e2982d6f8a9f', u'Title': u'洗发护发'},
                {u'TypeId': u'65140b4b-8e84-4abc-83f1-b37e0207d1ab', u'Title': u'口腔护理'},
                {u'TypeId': u'86a34137-990d-4e94-961c-f2441805ad3b', u'Title': u'女性护理'},
                {u'TypeId': u'a7fbfab7-8c6b-4083-9cf7-3b67848d936e', u'Title': u'身体护理'}], u'Title': u'洗护'},
            {u'TypeId': u'31ae92a4-5c66-4fc2-ac5b-b3ac1a7270d9',
            u'list': [{u'TypeId': u'45f92b04-5614-4f82-bb05-4c3bce2612b7', u'Title': u'中性香水'},
                {u'TypeId': u'c842a8c7-0b25-4e3b-9164-21601da1fd50', u'Title': u'Q版香水'},
                {u'TypeId': u'd1bdfe8a-3e3e-47fe-b839-bb0a499d00cd', u'Title': u'男士香水'},
                {u'TypeId': u'd71fdb80-eaef-41d2-acdf-012b8340609b', u'Title': u'女士香水'}], u'Title': u'香氛'},
            {u'TypeId': u'4a4cd77a-3316-4e83-b3d6-e20233d1b316',
            u'list': [{u'TypeId': u'0618cba4-04ea-4576-99a3-481e0a17b036', u'Title': u'眼部'},
                {u'TypeId': u'0803d3fe-45c2-420e-846d-9a0d1babde7c', u'Title': u'卸妆'},
                {u'TypeId': u'2e5169b9-3fc4-4541-b87c-aaf72199714e', u'Title': u'腮红'},
                {u'TypeId': u'3e603da6-0dea-44ea-b746-b2b8ec53ff1d', u'Title': u'遮瑕/修容'},
                {u'TypeId': u'44612fc6-9ae2-45df-81de-3387eaea0c61', u'Title': u'底妆'},
                {u'TypeId': u'504698c7-cf14-4d19-b6d3-2584c4af9362', u'Title': u'美甲'},
                {u'TypeId': u'5d471303-ce0b-41fa-b50d-17716cdbfcc3', u'Title': u'粉饼/散粉'},
                {u'TypeId': u'a8f7c4a5-ff87-43c7-bdde-031447fa6b9a', u'Title': u'工具'},
                {u'TypeId': u'af219275-1782-4e82-8e93-11907eb17d2f', u'Title': u'唇部'},
                {u'TypeId': u'b4bae5ec-e399-4f39-9a6c-023978eb4d67', u'Title': u'眉部'},
                {u'TypeId': u'e46b5874-7339-4519-8633-ec033da75bce', u'Title': u'隔离'},
                {u'TypeId': u'f0cad439-bae7-4617-b157-e3c3e1d70129', u'Title': u'睫毛'},
                {u'TypeId': u'f670db8b-89ed-412b-81e7-db6cec739787', u'Title': u'防晒'}], u'Title': u'彩妆'}]
        '''
        '''
        Input:?TypeId=&OrderType=DESC&OrderName=host&PageNum=1
        Output:[
            {u'TypeId': u'0a14b2b5-a4b4-48f7-a428-f2829e654324',
            u'list': [{u'TypeId': u'03ba13bb-7ca1-418f-87d2-f3a55904053d', u'Title': u'T区/特殊护理'},
                {u'TypeId': u'11dc2759-394f-4546-8a0c-3d22644cab97', u'Title': u'眼部护理'},
                {u'TypeId': u'171727e8-b6ad-4530-a024-52b312edd481', u'Title': u'洁面'},
                {u'TypeId': u'1cc37c7b-1a76-4be3-a1f3-818df09d0323', u'Title': u'精华'},
                {u'TypeId': u'a3e56d11-687d-4af8-b611-1add67d750fb', u'Title': u'面霜'},
                {u'TypeId': u'dac6eef7-c49d-4637-8c1d-052b439c5d46', u'Title': u'唇部护理'},
                {u'TypeId': u'dde8f3cb-c07c-43c8-93c0-06779d622462', u'Title': u'啫喱/凝露/凝胶'},
                {u'TypeId': u'e1486e88-1794-429d-af25-a1972f32e133', u'Title': u'化妆水/爽肤水'},
                {u'TypeId': u'efd47bdb-8bd5-4cc0-a865-7357fdfc3c36', u'Title': u'面膜'},
                {u'TypeId': u'f0cff16e-c5a2-40fe-8a73-f19c2c2a9df5', u'Title': u'乳液'},
                {u'TypeId': u'f43603f8-bd20-4c64-adf3-4f1203ba1875', u'Title': u'精油'}], u'Title': u'护肤'},
            {u'TypeId': u'1fe29d79-d37b-4a70-87c3-08e13169683f',
            u'list': [{u'TypeId': u'4e4bea3f-8a61-47a9-a786-e2982d6f8a9f', u'Title': u'洗发护发'},
                {u'TypeId': u'65140b4b-8e84-4abc-83f1-b37e0207d1ab', u'Title': u'口腔护理'},
                {u'TypeId': u'86a34137-990d-4e94-961c-f2441805ad3b', u'Title': u'女性护理'},
                {u'TypeId': u'a7fbfab7-8c6b-4083-9cf7-3b67848d936e', u'Title': u'身体护理'}], u'Title': u'洗护'},
            {u'TypeId': u'31ae92a4-5c66-4fc2-ac5b-b3ac1a7270d9',
            u'list': [{u'TypeId': u'45f92b04-5614-4f82-bb05-4c3bce2612b7', u'Title': u'中性香水'},
                {u'TypeId': u'c842a8c7-0b25-4e3b-9164-21601da1fd50', u'Title': u'Q版香水'},
                {u'TypeId': u'd1bdfe8a-3e3e-47fe-b839-bb0a499d00cd', u'Title': u'男士香水'},
                {u'TypeId': u'd71fdb80-eaef-41d2-acdf-012b8340609b', u'Title': u'女士香水'}], u'Title': u'香氛'},
            {u'TypeId': u'4a4cd77a-3316-4e83-b3d6-e20233d1b316',
            u'list': [{u'TypeId': u'0618cba4-04ea-4576-99a3-481e0a17b036', u'Title': u'眼部'},
                {u'TypeId': u'0803d3fe-45c2-420e-846d-9a0d1babde7c', u'Title': u'卸妆'},
                {u'TypeId': u'2e5169b9-3fc4-4541-b87c-aaf72199714e', u'Title': u'腮红'},
                {u'TypeId': u'3e603da6-0dea-44ea-b746-b2b8ec53ff1d', u'Title': u'遮瑕/修容'},
                {u'TypeId': u'44612fc6-9ae2-45df-81de-3387eaea0c61', u'Title': u'底妆'},
                {u'TypeId': u'504698c7-cf14-4d19-b6d3-2584c4af9362', u'Title': u'美甲'},
                {u'TypeId': u'5d471303-ce0b-41fa-b50d-17716cdbfcc3', u'Title': u'粉饼/散粉'},
                {u'TypeId': u'a8f7c4a5-ff87-43c7-bdde-031447fa6b9a', u'Title': u'工具'},
                {u'TypeId': u'af219275-1782-4e82-8e93-11907eb17d2f', u'Title': u'唇部'},
                {u'TypeId': u'b4bae5ec-e399-4f39-9a6c-023978eb4d67', u'Title': u'眉部'},
                {u'TypeId': u'e46b5874-7339-4519-8633-ec033da75bce', u'Title': u'隔离'},
                {u'TypeId': u'f0cad439-bae7-4617-b157-e3c3e1d70129', u'Title': u'睫毛'},
                {u'TypeId': u'f670db8b-89ed-412b-81e7-db6cec739787', u'Title': u'防晒'}], u'Title': u'彩妆'}]
        '''
        '''
        Input:
        Output:[
            {u'TypeId': u'0a14b2b5-a4b4-48f7-a428-f2829e654324',
            u'list': [{u'TypeId': u'03ba13bb-7ca1-418f-87d2-f3a55904053d', u'Title': u'T区/特殊护理'},
                {u'TypeId': u'11dc2759-394f-4546-8a0c-3d22644cab97', u'Title': u'眼部护理'},
                {u'TypeId': u'171727e8-b6ad-4530-a024-52b312edd481', u'Title': u'洁面'},
                {u'TypeId': u'1cc37c7b-1a76-4be3-a1f3-818df09d0323', u'Title': u'精华'},
                {u'TypeId': u'a3e56d11-687d-4af8-b611-1add67d750fb', u'Title': u'面霜'},
                {u'TypeId': u'dac6eef7-c49d-4637-8c1d-052b439c5d46', u'Title': u'唇部护理'},
                {u'TypeId': u'dde8f3cb-c07c-43c8-93c0-06779d622462', u'Title': u'啫喱/凝露/凝胶'},
                {u'TypeId': u'e1486e88-1794-429d-af25-a1972f32e133', u'Title': u'化妆水/爽肤水'},
                {u'TypeId': u'efd47bdb-8bd5-4cc0-a865-7357fdfc3c36', u'Title': u'面膜'},
                {u'TypeId': u'f0cff16e-c5a2-40fe-8a73-f19c2c2a9df5', u'Title': u'乳液'},
                {u'TypeId': u'f43603f8-bd20-4c64-adf3-4f1203ba1875', u'Title': u'精油'}], u'Title': u'护肤'},
            {u'TypeId': u'1fe29d79-d37b-4a70-87c3-08e13169683f',
            u'list': [{u'TypeId': u'4e4bea3f-8a61-47a9-a786-e2982d6f8a9f', u'Title': u'洗发护发'},
                {u'TypeId': u'65140b4b-8e84-4abc-83f1-b37e0207d1ab', u'Title': u'口腔护理'},
                {u'TypeId': u'86a34137-990d-4e94-961c-f2441805ad3b', u'Title': u'女性护理'},
                {u'TypeId': u'a7fbfab7-8c6b-4083-9cf7-3b67848d936e', u'Title': u'身体护理'}], u'Title': u'洗护'},
            {u'TypeId': u'31ae92a4-5c66-4fc2-ac5b-b3ac1a7270d9',
            u'list': [{u'TypeId': u'45f92b04-5614-4f82-bb05-4c3bce2612b7', u'Title': u'中性香水'},
                {u'TypeId': u'c842a8c7-0b25-4e3b-9164-21601da1fd50', u'Title': u'Q版香水'},
                {u'TypeId': u'd1bdfe8a-3e3e-47fe-b839-bb0a499d00cd', u'Title': u'男士香水'},
                {u'TypeId': u'd71fdb80-eaef-41d2-acdf-012b8340609b', u'Title': u'女士香水'}], u'Title': u'香氛'},
            {u'TypeId': u'4a4cd77a-3316-4e83-b3d6-e20233d1b316',
            u'list': [{u'TypeId': u'0618cba4-04ea-4576-99a3-481e0a17b036', u'Title': u'眼部'},
                {u'TypeId': u'0803d3fe-45c2-420e-846d-9a0d1babde7c', u'Title': u'卸妆'},
                {u'TypeId': u'2e5169b9-3fc4-4541-b87c-aaf72199714e', u'Title': u'腮红'},
                {u'TypeId': u'3e603da6-0dea-44ea-b746-b2b8ec53ff1d', u'Title': u'遮瑕/修容'},
                {u'TypeId': u'44612fc6-9ae2-45df-81de-3387eaea0c61', u'Title': u'底妆'},
                {u'TypeId': u'504698c7-cf14-4d19-b6d3-2584c4af9362', u'Title': u'美甲'},
                {u'TypeId': u'5d471303-ce0b-41fa-b50d-17716cdbfcc3', u'Title': u'粉饼/散粉'},
                {u'TypeId': u'a8f7c4a5-ff87-43c7-bdde-031447fa6b9a', u'Title': u'工具'},
                {u'TypeId': u'af219275-1782-4e82-8e93-11907eb17d2f', u'Title': u'唇部'},
                {u'TypeId': u'b4bae5ec-e399-4f39-9a6c-023978eb4d67', u'Title': u'眉部'},
                {u'TypeId': u'e46b5874-7339-4519-8633-ec033da75bce', u'Title': u'隔离'},
                {u'TypeId': u'f0cad439-bae7-4617-b157-e3c3e1d70129', u'Title': u'睫毛'},
                {u'TypeId': u'f670db8b-89ed-412b-81e7-db6cec739787', u'Title': u'防晒'}], u'Title': u'彩妆'}]
        '''
        response = self.fetch(
            "/v1/goods/categories", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_get_goods_classify(json_data)

    def _check_get_goods_classify(self, json_data):
        if json_data:
            print "ApiGetGoodsClassify:", json_data


class ApiAppLimitedGoodsListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppLimitedGoodsListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppLimitedGoodsListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_limited_goods_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:{
          "status": "success",
          "today_limited_goods": [
            {
              "goods_limited_intro": "韩妮采眼线笔，最防晕最防水最持久的眼线笔！ 真的一点不夸张，涂上的瞬间马上干掉，然后就屹立不倒的在那里了， 除了眼唇卸妆产品能擦掉之外，没有能让它晕开的！！ 必须用眼唇卸妆卸！",
              "goods_id": "02eabb87-c4cc-4829-a251-34081cd641ef",
              "goods_name": "heynature韩妮采防水啫喱眼线笔NO.1黑色",
              "goods_limited_price": "58",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/02eabb87-c4cc-4829-a251-34081cd641ef/goods/e16d0bf4-cdc4-493a-8e32-e7f3636e9dcc.JPG",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "goods_left_count": 0,
              "goods_original_price": "324.00"
            },
            ...
          ],
          "message": "",
          "tomorrow_limited_goods": []
        }
        '''
        response = self.fetch(
            "/v1/home_limited", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_app_limited_goods_list(json_data)

    def _check_api_app_limited_goods_list(self, json_data):
        if json_data:
            print "ApiAppLimitedGoodsListHandler:", json_data


class ApiAppNewGoodsListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppNewGoodsListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppNewGoodsListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_new_goods_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "goods_limited_intro": "以乳酸、甘醇酸、酵母萃取，搭配有機蘆薈萃取等溫和天然配方，不含水楊酸不傷肌膚，自然軟化足部角質，1次使用、7天見效，輕鬆解決足部老廢腳皮、乾燥粗糙、老繭、腳氣、膚色不均…等問題！",
              "goods_id": "0bccb166-86c8-4576-89be-4daaeb5ddb77",
              "goods_name": "奇拉朵 Kiladoll 魔力去角质嫩白足膜 1对/盒",
              "goods_limited_price": "40.00",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/0bccb166-86c8-4576-89be-4daaeb5ddb77/goods/6619dc98-dc58-4e98-99b7-621a1fbe912e.JPG",
              "country_img_url": "http://s.meihuishuo.com/images/country/tw.png",
              "goods_left_count": 8,
              "goods_original_price": "80.00"
            },
            {
              "goods_limited_intro": "韩妮采眼线笔，最防晕最防水最持久的眼线笔！ 真的一点不夸张，涂上的瞬间马上干掉，然后就屹立不倒的在那里了， 除了眼唇卸妆产品能擦掉之外，没有能让它晕开的！！ 必须用眼唇卸妆卸！",
              "goods_id": "02eabb87-c4cc-4829-a251-34081cd641ef",
              "goods_name": "heynature韩妮采防水啫喱眼线笔NO.1黑色",
              "goods_limited_price": "58",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/02eabb87-c4cc-4829-a251-34081cd641ef/goods/e16d0bf4-cdc4-493a-8e32-e7f3636e9dcc.JPG",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "goods_left_count": 0,
              "goods_original_price": "324.00"
            },
            ...
          ]
        }
        '''
        response = self.fetch(
            "/v1/home_new", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_app_new_goods_list(json_data)

    def _check_api_app_new_goods_list(self, json_data):
        if json_data:
            print "ApiAppNewGoodsListHandlerTest:", json_data


class ApiAppEssenceGoodsListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppEssenceGoodsListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppEssenceGoodsListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_essence_goods_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "goods_limited_intro": "韩国济州岛芦荟精华，99%芦荟萃取，晒后修复，美白保湿，绿色无添加。\r\n爱美的菇凉们，当日特价推送宝贝，您只能领取一件回家哦！因为我们的app还年幼，请谅解思密达！要是你手滑，重复购买多次，我们只给你发一件货哦，余款给你打回去。",
              "goods_id": "ac3d712e-bc84-42c4-83b0-43ffd680ad13",
              "goods_name": "NICEFACE牛角芦荟胶250ML",
              "goods_limited_price": "58",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/ac3d712e-bc84-42c4-83b0-43ffd680ad13/goods/5bc95646-961b-4a78-84a8-f6e4b4f96324.JPG",
              "country_img_url": "http://s.meihuishuo.com/images/country/tw.png",
              "goods_left_count": 8,
              "goods_original_price": "None"
            },
            {
              "goods_limited_intro": "独特的滚动刷头设计，遮瑕性更强，让粗大毛孔细纹斑点消失无影。 用按钮控制的滚动粉扑一体容器液态BB。 内含摩洛哥坚果油和夏威夷海洋深层水。滋润皮肤，演绎贵族皮肤。\r\n\r\n-----------------------------------------------------\r\n   保税区商品，订单总价≤100元即可免征关税\r\n          本商品单件直接下单可免税啦！\r\n     订单总价超过100元将收取50%关税哦！\r\n-----------------------------------------------------",
              "goods_id": "02dbf97b-811f-4739-80b2-08709a6dd16d",
              "goods_name": "(保税) HolikaHolika滚动滚轮BB霜30ml/支21号象牙白色",
              "goods_limited_price": "89.90",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/02dbf97b-811f-4739-80b2-08709a6dd16d/goods/d2fba1be-650e-447d-b260-02b5c5928377.JPG",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "goods_left_count": 100,
              "goods_original_price": "None"
            },
            ...
          ]
        }
        '''
        response = self.fetch(
            "/v1/home_picks", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_app_essence_goods_list(json_data)

    def _check_api_app_essence_goods_list(self, json_data):
        if json_data:
            print "ApiAppEssenceGoodsListHandlerTest:", json_data


class ApiAppAdvertisementImgListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppAdvertisementImgListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppAdvertisementImgListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_advertisement_img_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:
        {
          "status": "success",
          "message": "",
          "ads": [
            {
              "adv_img_url": "http://slocal.meihuishuo.com:8080/photos/raw/89/8901f172721549149175f4f3990994dc.jpg",
              "id": 644
            },
            {
              "adv_img_url": "http://slocal.meihuishuo.com:8080/photos/raw/63/63914c7323f84f32ae0653fa97f8a944.jpg",
              "id": 645
            },
            {
              "adv_img_url": "http://slocal.meihuishuo.com:8080/photos/raw/c5/c55c0070a7b346f6887018379a5b3b68.jpg",
              "id": 643
            }
          ]
        }
        '''
        response = self.fetch(
            "/v1/home_ads", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_app_advertisement_img_list(json_data)

    def _check_api_app_advertisement_img_list(self, json_data):
        if json_data:
            print "ApiAppAdvertisementImgListHandlerTest:", json_data


class ApiAppAdvertisementGoodsHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppAdvertisementGoodsHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppAdvertisementGoodsHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_advertisement_goods(self):
        # request_body = urllib.urlencode()
        '''
        Input:parent_id = 643
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "Korea  韩国原装",
              "goods_name": "'可莱丝NMF水库睡眠面膜深蓝15ml*5 ",
              "goods_id": "fe6c5570-ac3b-4d4a-a91b-920baf258ce9",
              "goods_limited_price": "59.9",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/fe6c5570-ac3b-4d4a-a91b-920baf258ce9/goods/c224c98f-a67a-4737-a8e1-62564bce465f.JPG",
              "buy_count": "674",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "is_sold_out": 0,
              "goods_original_price": "None",
              "stock": 10
            },
            ...
          ],
          "adv_img_url": "http://slocal.meihuishuo.com:8080/photos/raw/c5/c55c0070a7b346f6887018379a5b3b68.jpg",
          "adv_title": "测试1"
        }
        '''
        '''
        Input:parent_id = 640
        Output:{
          "status": "error",
          "message": "请求数据不存在"
        }
        '''
        '''
        Input:parent_id = dsfsdfsd
        Output:{
          "status": "error",
          "message": "请求数据不存在"
        }
        '''
        response = self.fetch(
            "/v1/home_ads/643", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_app_advertisement_goods(json_data)

    def _check_api_app_advertisement_goods(self, json_data):
        if json_data:
            print "ApiAppAdvertisementGoodsHandlerTest:", json_data


class ApiAppHomeCatesHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppHomeCatesHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppHomeCatesHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_app_home_cates(self):
        # request_body = urllib.urlencode()
        '''
        Input:promo_type = cates_new/cates_asia/cates_eu_us/cates_tax_free
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "U.S.A  美国（具体产地以收到的实物为准）原装",
              "goods_name": "雅诗兰黛 (Estee Lauder) 红石榴日霜 50ml",
              "goods_id": "02c6188d-9cfb-482e-aa2c-4bed8d4b0946",
              "goods_limited_price": "442.50",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/02c6188d-9cfb-482e-aa2c-4bed8d4b0946/goods/d26c3071-f7ac-4f2d-b6bb-a4e7e768ba59.JPG",
              "buy_count": "546",
              "country_img_url": "http://s.meihuishuo.com/images/country/us.png",
              "is_sold_out": 0,
              "goods_original_price": "None",
              "stock": 4
            },
            ...
          ]
        }
        '''
        '''
        Input:promo_type = cates
        Output:{
          "status": "error",
          "message": "请求失败"
        }
        '''
        '''
        Input:promo_type = cates_new/cates_asia/cates_eu_us/cates_tax_free?start=0
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "U.S.A  美国（具体产地以收到的实物为准）原装",
              "goods_name": "雅诗兰黛 (Estee Lauder) 红石榴日霜 50ml",
              "goods_id": "02c6188d-9cfb-482e-aa2c-4bed8d4b0946",
              "goods_limited_price": "442.50",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/02c6188d-9cfb-482e-aa2c-4bed8d4b0946/goods/d26c3071-f7ac-4f2d-b6bb-a4e7e768ba59.JPG",
              "buy_count": "546",
              "country_img_url": "http://s.meihuishuo.com/images/country/us.png",
              "is_sold_out": 0,
              "goods_original_price": "None",
              "stock": 4
            },
            ...
          ]
        }
        '''
        '''
        Input:promo_type = cates_new/cates_asia/cates_eu_us/cates_tax_free?start=0dfsdsd
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "U.S.A  美国（具体产地以收到的实物为准）原装",
              "goods_name": "雅诗兰黛 (Estee Lauder) 红石榴日霜 50ml",
              "goods_id": "02c6188d-9cfb-482e-aa2c-4bed8d4b0946",
              "goods_limited_price": "442.50",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/02c6188d-9cfb-482e-aa2c-4bed8d4b0946/goods/d26c3071-f7ac-4f2d-b6bb-a4e7e768ba59.JPG",
              "buy_count": "546",
              "country_img_url": "http://s.meihuishuo.com/images/country/us.png",
              "is_sold_out": 0,
              "goods_original_price": "None",
              "stock": 4
            },
            ...
          ]
        }
        '''
        response = self.fetch(
            "/v1/home_cates/cates_new", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_app_home_cates(json_data)

    def _check_api_app_home_cates(self, json_data):
        if json_data:
            print "ApiAppHomeCatesHandlerTest:", json_data


class ApiSearchListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiSearchListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiSearchListHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_home.urls
        )

    def test_api_search_list(self):
        # request_body = urllib.urlencode()
        '''
        Input:
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "韩国  韩国原装",
              "goods_id": "157d83e1-4800-424a-b86e-b458b8a7eac4",
              "goods_name": "后whoo 拱辰享 气津 阴阳 平衡水乳小样",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/157d83e1-4800-424a-b86e-b458b8a7eac4/goods/ab7ce31b-f01a-4d55-a9d5-e8c54fd33d1b.JPG",
              "price": "99",
              "buy_count": "0",
              "goods_brief_intro": "拱辰享 气津 阴阳 平衡水乳",
              "discount": "",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "domestic_price": "99",
              "stock_count": "10"
            },
            ...
          ]
        }
        '''
        '''
        Input:?search=后&page_num=1
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "韩国  韩国原装",
              "goods_id": "157d83e1-4800-424a-b86e-b458b8a7eac4",
              "goods_name": "后whoo 拱辰享 气津 阴阳 平衡水乳小样",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/157d83e1-4800-424a-b86e-b458b8a7eac4/goods/ab7ce31b-f01a-4d55-a9d5-e8c54fd33d1b.JPG",
              "price": "99",
              "buy_count": "0",
              "goods_brief_intro": "拱辰享 气津 阴阳 平衡水乳",
              "discount": "",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "domestic_price": "99",
              "stock_count": "10"
            },
            ...
          ]
        }
        '''
        '''
        Input:?search=后&page_num=2
        Output: {
          "status": "success",
          "message": "没有你要搜索的商品"
        }
        '''
        '''
        Input:?search=后
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "韩国  韩国原装",
              "goods_id": "157d83e1-4800-424a-b86e-b458b8a7eac4",
              "goods_name": "后whoo 拱辰享 气津 阴阳 平衡水乳小样",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/157d83e1-4800-424a-b86e-b458b8a7eac4/goods/ab7ce31b-f01a-4d55-a9d5-e8c54fd33d1b.JPG",
              "price": "99",
              "buy_count": "0",
              "goods_brief_intro": "拱辰享 气津 阴阳 平衡水乳",
              "discount": "",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "domestic_price": "99",
              "stock_count": "10"
            },
            ...
          ]
        }
        '''
        '''
        Input:?search=后&page_num=1&order_name=price
        Output:{
          "status": "success",
          "message": "",
          "goods": [
            {
              "country_intro": "韩国  韩国原装",
              "goods_id": "3eca5512-57bc-445a-bb29-2372afbf6953",
              "goods_name": "Accine皇后EGF黑珍珠眼贴膜60片",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/3eca5512-57bc-445a-bb29-2372afbf6953/goods/77765054-277d-4284-a91c-eb3fa7f78bb6.JPG",
              "price": "79",
              "buy_count": "1124",
              "goods_brief_intro": "Accine皇后EGF黑珍珠眼贴膜",
              "discount": "",
              "country_img_url": "http://s.meihuishuo.com/images/country/kr.png",
              "domestic_price": "147",
              "stock_count": "141"
            },
            {
              "country_intro": "日本  日本原装",
              "goods_id": "be274111-de9a-411d-bc15-8b9a2625ab59",
              "goods_name": "ALOVIVI皇后卸妆水500ml",
              "goods_img_url": "http://123.56.109.37:8080/beautalk/localfile/be274111-de9a-411d-bc15-8b9a2625ab59/goods/65edeb7e-fc10-4cb1-ac42-d392e234bb0d.JPG",
              "price": "82",
              "buy_count": "1274",
              "goods_brief_intro": "皇后卸妆水 500ml",
              "discount": "",
              "country_img_url": "http://s.meihuishuo.com/images/country/jp.png",
              "domestic_price": "170",
              "stock_count": "60"
            },
            ...
          ]
        }
        '''
        response = self.fetch(
            "/v1/search", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_search_list(json_data)

    def _check_api_search_list(self, json_data):
        if json_data:
            print "ApiSearchListHandlerTest:", json_data


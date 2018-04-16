#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib
import unittest
import tornado.testing
import tornado.httpclient

import meihuishuo.handlers.api.api_shop as handler_api_shop

from meihuishuo.tests.test_base import BaseHTTPTestCase


class CommonCheck(object):
    pass


class ApiAppShopHomeHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAppShopHomeHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAppShopHomeHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_shop.urls
        )

    def test_api_app_shop_home(self):
        '''
        Input:
        Output:[
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/home/f69f91de-b426-4c02-b036-05b427bf99da.JPG',
            u'RelatedId': u'5bb1655b-18ce-400e-8d03-81d64af5b70a', u'IfMiddlePage': None, u'CommodityText': None}
            ]
        '''
        response = self.fetch(
            "/v1/brands/home", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_app_shop_home(json_data)


    def _check_app_shop_home(self, json_data):
        if json_data:
            print "ApiAppShopHome:", json_data


class ApiFindBrandAreaTypeHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindBrandAreaTypeHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindBrandAreaTypeHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_shop.urls
        )

    def test_api_find_brand_area_type(self):
        '''
        Input:
        Output:[
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/c858c1c5-425b-4816-bc89-15d5ed0f512f.JPG',
            u'GoodsTypeName': u'护肤', u'GoodsType': u'0a14b2b5-a4b4-48f7-a428-f2829e654324'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/d1b4b352-7477-4e44-afd5-6011f1a427d6.JPG',
            u'GoodsTypeName': u'彩妆', u'GoodsType': u'4a4cd77a-3316-4e83-b3d6-e20233d1b316'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/0c05a393-cf37-44b8-90fa-56a91705abba.JPG',
            u'GoodsTypeName': u'洁面', u'GoodsType': u'171727e8-b6ad-4530-a024-52b312edd481'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/120e8f9e-9c14-4f4e-87af-b028cddba3e4.JPG',
            u'GoodsTypeName': u'洗护', u'GoodsType': u'1fe29d79-d37b-4a70-87c3-08e13169683f'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/685a2223-58cb-41e9-84d7-e51a143498c2.JPG',
            u'GoodsTypeName': u'防晒', u'GoodsType': u'f670db8b-89ed-412b-81e7-db6cec739787'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/701a9fed-d9a0-42f9-abff-216b8735881c.JPG',
            u'GoodsTypeName': u'面膜', u'GoodsType': u'efd47bdb-8bd5-4cc0-a865-7357fdfc3c36'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/4460a87b-d771-45a4-bd14-bae0241ac3c6.JPG',
            u'GoodsTypeName': u'唇部', u'GoodsType': u'af219275-1782-4e82-8e93-11907eb17d2f'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/94173761-b092-436d-a501-35beb1eefe77.JPG',
            u'GoodsTypeName': u'乳液', u'GoodsType': u'f0cff16e-c5a2-40fe-8a73-f19c2c2a9df5'}
            ]
        '''
        response = self.fetch(
            "/v1/brands/types", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_brand_area_type(json_data)


    def _check_find_brand_area_type(self, json_data):
        if json_data:
            print "ApiFindBrandAreaType:", json_data


class ApiAsianBrandHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiAsianBrandHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiAsianBrandHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_shop.urls
        )

    def test_api_asian_brand(self):
        '''
        Input:
        Output:
        '''
        response = self.fetch(
            "/v1/brands/asia", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_asian_brand(json_data)


    def _check_asian_brand(self, json_data):
        if json_data:
            print "ApiAsianBrand:", json_data


class ApiEuropeanBrandHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiEuropeanBrandHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiEuropeanBrandHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_shop.urls
        )

    def test_api_european_brand(self):
        '''
        Input:
        Output:
        '''
        response = self.fetch(
            "/v1/brands/european", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_european_brand(json_data)


    def _check_european_brand(self, json_data):
        if json_data:
            print "ApiEuropeanBrand:", json_data


class ApiFindBrandareanewHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindBrandareanewHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindBrandareanewHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    def set_handlers(self):
        self.app.add_handlers(
            self.app.settings["api_domain"], handler_api_shop.urls
        )

    def test_api_find_brandareanew(self):
        '''
        Input:
        Output:[
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/1e3683b9-50e5-4f73-99c5-d702e6f8d34e.JPG',
            u'ShopId': u'67625f69-883c-45e2-a57e-15a806bac00c', u'CommodityText': u'VDL'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/132256b0-6265-4d59-8c2f-c69cc0ad0a64.JPG',
            u'ShopId': u'd42d5d0d-1e11-4682-abe8-88d7a2ea2569', u'CommodityText': u'九朵云'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/358e065d-e4e2-4dba-afd6-d36d201392a0.JPG',
            u'ShopId': u'a8ab36ae-c611-43c8-b3de-d51c4bafa24b', u'CommodityText': u'too cool for school'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/e858fa90-de64-47b7-93c7-46d5b2387e75.JPG',
            u'ShopId': u'80a157da-fa83-49ee-868e-ac6c635b63f3', u'CommodityText': u'可莱丝'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/1288dbf5-77c0-4597-af67-e6ef85f911ff.JPG',
            u'ShopId': u'8dd985fd-fe6c-4ef2-bf3e-6c8867edbb86', u'CommodityText': u'Dongkook'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/classify/8632fb57-7967-4702-a996-6e0c43f842a1.JPG',
            u'ShopId': u'8c177696-43da-495f-a19b-94cda72f354c', u'CommodityText': u'Holika Holika'}
            ]
        '''
        response = self.fetch(
            "/v1/brands/new", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_brandareanew(json_data)


    def _check_find_brandareanew(self, json_data):
        if json_data:
            print "ApiFindBrandareanew:", json_data


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
# import urllib
from urllib import parse as urllib
import unittest
import tornado.testing
import tornado.httpclient

# import meihuishuo.handlers.api.api_order as handler_api_orders

from app.tests.test_base import BaseHTTPTestCase


class CommonCheck(object):
    pass


class ApiMyOrderHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiMyOrderHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiMyOrderHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_api_my_order(self):
        # request_body = urllib.urlencode()
        # ?MemberId=da49503e8a3aa12&Status=4(Result: Return Order detail. The detail include OrderId, Status, CreateDate, GoodsList, AllPrice)
        # ?MemberId=da49503e8a3aa12&Status=2(Result: Return [])
        # ?MemberId=da49503e8a3aa13&Status=4(Result: Return [])
        # ?MemberId=&Status=(Result: Return [])
        # ?MemberId=68df7c34e8eb981&Status=1(Result: Return all order lists and goods list.)
        response = self.fetch(
            "/v1/orders/?MemberId=da49503e8a3aa12&Status=2", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_my_order(json_data)


    def _check_my_order(self, json_data):
        if json_data:
            print("MyOrder:", json_data)


class ApiInsertIosHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiInsertIosHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiInsertIosHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_api_insert_ios(self):
        '''
        GoodsInfo: {
            "MemberId":"01aee9ee653c4dc","CollectPerson":"zmxu","CollectAddress":"广东深圳",
            "CollectTel":"13829572460","DeliverTime":"1","Price":"￥181.0","DeliverCost":"0.0",
            "Distribution":"1","LoginType":"android","GoodsList":[{
                "GoodsCount": "1",
                "GrouponId": "",
                "ActivityId": "",
                "Weight": "113",
                "GoodsId": "6168638a-2ac5-44b9-861e-d8c559263985",
                "ImgView": "http://123.56.109.37:8080/beautalk/localfile/6168638a-2ac5-44b9-861e-d8c559263985/goods/a6b97284-d73d-4178-8716-7067736e9b00.JPG",
                "Price": "￥65.0",
                "DomesticPrice": "128",
                "Discount": "",
                "Stock": "10",
                "Abbreviation": "destine婴儿护臀膏113g-护肤型（蓝色）",
                "Title": "destine婴儿护臀膏113g-护肤型（蓝色）",
                "PriceAndCount": "￥65.0 X 1"
                },
                {
                "GoodsCount": "2",
                "GrouponId": "b924bb6a-1325-4dd8-b87d-833df853c8ca",
                "ActivityId": "05866e16-59f9-4e60-b0ec-d777b7c1f3d3",
                "Weight": "3.5",
                "GoodsId": "7b342345-d01c-4ec2-bbf2-c3449c026512",
                "ImgView": "http://123.56.109.37:8080/beautalk/localfile/7b342345-d01c-4ec2-bbf2-c3449c026512/goods/608c401a-3ea3-4cf5-8574-58c1f8e0e3c1.PNG",
                "Price": "￥58.0",
                "DomesticPrice": "98",
                "Discount": "5.9",
                "Stock": "6",
                "Abbreviation": "爱丽小屋水凝心机液体唇膏OR201 3.5g",
                "Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g",
                "PriceAndCount": "￥58.0 X 2"
                }
            ]}
        Result: order_model has a new order record, and order_goods has goods list record which order_id equal order record's order_od.
                And order_status model has a record for order, delete shop_cart record. Return success message.
        '''
        '''
        GoodsInfo: None
        Result: "订单好为空"
        '''
        '''
        GoodsInfo: not json data
        Result: "订单数据不正确"
        '''
        '''
        GoodsInfo: GoodsList is []
        Result: "订单商品数据为空"
        '''
        '''
        GoodsInfo: GoodsList is []
        Result: "订单商品数据为空"
        '''
        '''
        GoodsInfo: Error Input
        Result: "订单数据有误"
        '''
        '''
        GoodsInfo: One good stock is 0
        Result: "下手晚了，您购买的商品中存在已售空的商品"
        '''
        request_body = urllib.urlencode(dict(GoodsInfo='{\
            "MemberId":"01aee9ee653c4dc",\
            "CollectPerson":"zmxu",\
            "CollectAddress":"广东深圳",\
            "CollectTel":"13829572460",\
            "DeliverTime":"1",\
            "Price":"￥181.0",\
            "DeliverCost":"0.0",\
            "Distribution":"1",\
            "LoginType":"android",\
            "GoodsList":\
            [{"GoodsCount": "1",\
            "GrouponId": "",\
            "ActivityId": "",\
            "Weight": "113",\
            "GoodsId": "6168638a-2ac5-44b9-861e-d8c559263985",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/6168638a-2ac5-44b9-861e-d8c559263985/goods/a6b97284-d73d-4178-8716-7067736e9b00.JPG",\
            "Price": "￥65.0",\
            "DomesticPrice": "128",\
            "Discount": "",\
            "Stock": "10",\
            "Abbreviation": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "Title": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "PriceAndCount": "￥65.0 X 1"\
            },\
            {\
            "GoodsCount": "2",\
            "GrouponId": "b924bb6a-1325-4dd8-b87d-833df853c8ca",\
            "ActivityId": "05866e16-59f9-4e60-b0ec-d777b7c1f3d3",\
            "Weight": "3.5",\
            "GoodsId": "7b342345-d01c-4ec2-bbf2-c3449c026512",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/7b342345-d01c-4ec2-bbf2-c3449c026512/goods/608c401a-3ea3-4cf5-8574-58c1f8e0e3c1.PNG",\
            "Price": "￥58.0",\
            "DomesticPrice": "98",\
            "Discount": "5.9",\
            "Stock": "6",\
            "Abbreviation": "爱丽小屋水凝心机液体唇膏OR201 3.5g",\
            "Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g","PriceAndCount": "￥58.0 X 2"}]}'))
        response = self.fetch(
            "/v1/orders/create", method="POST", body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_insert_ios(json_data)

    def _check_insert_ios(self, json_data):
        if json_data:
            print("InsertIos", json_data)


class ApiUpdateOrderHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiUpdateOrderHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiUpdateOrderHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_update_order_ios(self):
        '''
        GoodsInfo:{"UUID":"20150806093429",\
            "MemberId":"01aee9ee653c4dc",\
            "CollectPerson":"zmxu_zmxu",\
            "CollectAddress":"广东深圳",\
            "CollectTel":"13829572460",\
            "DeliverTime":"1",\
            "Price":"￥181.0",\
            "DeliverCost":"0.0",\
            "Distribution":"1",\
            "LoginType":"android",\
            "GoodsList":\
            [{"GoodsCount": "1",\
            "GrouponId": "",\
            "ActivityId": "",\
            "Weight": "113",\
            "GoodsId": "6168638a-2ac5-44b9-861e-d8c559263985",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/6168638a-2ac5-44b9-861e-d8c559263985/goods/a6b97284-d73d-4178-8716-7067736e9b00.JPG",\
            "Price": "￥65.0",\
            "DomesticPrice": "128",\
            "Discount": "",\
            "Stock": "10",\
            "Abbreviation": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "Title": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "PriceAndCount": "￥65.0 X 1"\
            },\
            {\
            "GoodsCount": "2",\
            "GrouponId": "b924bb6a-1325-4dd8-b87d-833df853c8ca",\
            "ActivityId": "05866e16-59f9-4e60-b0ec-d777b7c1f3d3",\
            "Weight": "3.5",\
            "GoodsId": "7b342345-d01c-4ec2-bbf2-c3449c026512",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/7b342345-d01c-4ec2-bbf2-c3449c026512/goods/608c401a-3ea3-4cf5-8574-58c1f8e0e3c1.PNG",\
            "Price": "￥58.0",\
            "DomesticPrice": "98",\
            "Discount": "5.9",\
            "Stock": "6",\
            "Abbreviation": "爱丽小屋水凝心机液体唇膏OR201 3.5g",\
            "Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g","PriceAndCount": "￥58.0 X 2"}]}
        Result: Return a map. The map include message, result, Distribution, AlipayAccount, countChange and PrivateKey.
        '''

        '''
        GoodsInfo: None
        Result: {"message": "订单不能为空","result": "error"}
        '''

        '''
        GoodsInfo:{"UUID":"20150806093429",\
            "MemberId":"01aee9ee653c4dc",\
            "CollectPerson":"zmxu_zmxu",\
            "CollectAddress":"广东深圳",\
            "CollectTel":"13829572460",\
            "DeliverTime":"1",\
            "Price":"￥181.0",\
            "DeliverCost":"0.0",\
            "Distribution":"1",\
            "LoginType":"android",\
            "GoodsList":\
            []}
        Result: {u'message': u'下手晚了，您购买的商品中存在已售空的商品', u'result': u'error'}
        '''

        '''
        GoodsInfo: {"UUID":"",\
            "MemberId":"01aee9ee653c4dc",\
            "CollectPerson":"zmxu_zmxu",\
            "CollectAddress":"广东深圳",\
            "CollectTel":"13829572460",\
            "DeliverTime":"1",\
            "Price":"￥181.0",\
            "DeliverCost":"0.0",\
            "Distribution":"1",\
            "LoginType":"android",\
            "GoodsList":\
            [{"GoodsCount": "1",\
            "GrouponId": "",\
            "ActivityId": "",\
            "Weight": "113",\
            "GoodsId": "6168638a-2ac5-44b9-861e-d8c559263985",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/6168638a-2ac5-44b9-861e-d8c559263985/goods/a6b97284-d73d-4178-8716-7067736e9b00.JPG",\
            "Price": "￥65.0",\
            "DomesticPrice": "128",\
            "Discount": "",\
            "Stock": "10",\
            "Abbreviation": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "Title": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "PriceAndCount": "￥65.0 X 1"\
            },\
            {\
            "GoodsCount": "2",\
            "GrouponId": "b924bb6a-1325-4dd8-b87d-833df853c8ca",\
            "ActivityId": "05866e16-59f9-4e60-b0ec-d777b7c1f3d3",\
            "Weight": "3.5",\
            "GoodsId": "7b342345-d01c-4ec2-bbf2-c3449c026512",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/7b342345-d01c-4ec2-bbf2-c3449c026512/goods/608c401a-3ea3-4cf5-8574-58c1f8e0e3c1.PNG",\
            "Price": "￥58.0",\
            "DomesticPrice": "98",\
            "Discount": "5.9",\
            "Stock": "6",\
            "Abbreviation": "爱丽小屋水凝心机液体唇膏OR201 3.5g",\
            "Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g","PriceAndCount": "￥58.0 X 2"}]}
        Result: {u'message': u'订单错误', u'result': u'error'}
        '''

        '''
        GoodsInfo:{"UUID":"20150806093429",\
            "MemberId":"",\
            "CollectPerson":"zmxu_zmxu",\
            "CollectAddress":"广东深圳",\
            "CollectTel":"13829572460",\
            "DeliverTime":"1",\
            "Price":"￥181.0",\
            "DeliverCost":"0.0",\
            "Distribution":"1",\
            "LoginType":"android",\
            "GoodsList":\
            [{"GoodsCount": "1",\
            "GrouponId": "",\
            "ActivityId": "",\
            "Weight": "113",\
            "GoodsId": "6168638a-2ac5-44b9-861e-d8c559263985",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/6168638a-2ac5-44b9-861e-d8c559263985/goods/a6b97284-d73d-4178-8716-7067736e9b00.JPG",\
            "Price": "￥65.0",\
            "DomesticPrice": "128",\
            "Discount": "",\
            "Stock": "10",\
            "Abbreviation": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "Title": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "PriceAndCount": "￥65.0 X 1"\
            },\
            {\
            "GoodsCount": "2",\
            "GrouponId": "b924bb6a-1325-4dd8-b87d-833df853c8ca",\
            "ActivityId": "05866e16-59f9-4e60-b0ec-d777b7c1f3d3",\
            "Weight": "3.5",\
            "GoodsId": "7b342345-d01c-4ec2-bbf2-c3449c026512",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/7b342345-d01c-4ec2-bbf2-c3449c026512/goods/608c401a-3ea3-4cf5-8574-58c1f8e0e3c1.PNG",\
            "Price": "￥58.0",\
            "DomesticPrice": "98",\
            "Discount": "5.9",\
            "Stock": "6",\
            "Abbreviation": "爱丽小屋水凝心机液体唇膏OR201 3.5g",\
            "Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g","PriceAndCount": "￥58.0 X 2"}]}
        Result: {u'Distribution': u'1', u'PrivateKey': \
            u'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAM/IFtMGdJDK0NMQ7YLOFEniMrBTEMV596FqnVNpTL+Q/\
            eccZxSO83AHDWZNqMv04p7Ksz9hA8g+2q41WPP5vMQUZbCF5cath8nXK8KeVNHpgVhIdEpdtpfH5uVDcEZADnsafEymCMn3ty\
            jHYKBPMv2MmQvrbdFB4Mup/t440d6BAgMBAAECgYEAraBZ0kUWqteP4I/IqQFj2sl16fm/jgT5dJ0OkmDvjTSvtqv5RyidLAP4\
            ooBKiQQ9Ssu/NTrwWiiLu/9AMb+CiCUp0QGCOzAl3cSxYmGLcJb3tfsFdZD83h4nqSAYmF6pDOy4aQfa5u/kt0CPKOKBqmuAi7\
            QaGCK0AcGr1bcV9AECQQDzteL0fxeCyLu0NcVibJXoziEfvXQfIkjX7MTSePwv9yT6K6zKYlr9DTXrkTxC9w8rHYtphJTa+0qvs\
            N7Iz+6RAkEA2kJjcF1U753zN7OO3L4POjvSV9Y6kZbDE+0A+RUXp8jmBV1Boq0m4joGIXgZkHBNFTKeiLpDsMq+hmxUWiHI8QJBA\
            JlFvivotl+hYTOwUahaBFn7Maflnd9qz4dFOG/qeSitdYsE5tIN042svkmd+NlgyiBin2hIYtnqCwm94g9HfpECQDUHWkertX4+fyBy\
            dOx3FRYOAM4sk7BZ0+3ccJcUI9o1OoXlIZRXw5HFjUXGe1eXoXLcCJ6putaSe/YHDfuUJ9ECQBUHStnh1IFbVbLekX48MDjpHgmWiK4\
            +VblNsm9O+eJPrWh6+yflkv4gW65APv8j5qtWdtAhRB0fRyoBKP6B2gg=', \
            u'message': u'提交成功', u'AlipayAccount': u'2088711790044496', u'result': u'success'}
        '''

        '''
        GoodsInfo:{"UUID":"20150806093429",\
            "MemberId":"",\
            "GoodsList":\
            [{"GoodsCount": "1",\
            "GrouponId": "",\
            "ActivityId": "",\
            "Weight": "113",\
            "GoodsId": "6168638a-2ac5-44b9-861e-d8c559263985",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/6168638a-2ac5-44b9-861e-d8c559263985/goods/a6b97284-d73d-4178-8716-7067736e9b00.JPG",\
            "Price": "￥65.0",\
            "DomesticPrice": "128",\
            "Discount": "",\
            "Stock": "10",\
            "Abbreviation": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "Title": "destine婴儿护臀膏113g-护肤型（蓝色）",\
            "PriceAndCount": "￥65.0 X 1"\
            },\
            {\
            "GoodsCount": "2",\
            "GrouponId": "b924bb6a-1325-4dd8-b87d-833df853c8ca",\
            "ActivityId": "05866e16-59f9-4e60-b0ec-d777b7c1f3d3",\
            "Weight": "3.5",\
            "GoodsId": "7b342345-d01c-4ec2-bbf2-c3449c026512",\
            "ImgView": "http://123.56.109.37:8080/beautalk/localfile/7b342345-d01c-4ec2-bbf2-c3449c026512/goods/608c401a-3ea3-4cf5-8574-58c1f8e0e3c1.PNG",\
            "Price": "￥58.0",\
            "DomesticPrice": "98",\
            "Discount": "5.9",\
            "Stock": "6",\
            "Abbreviation": "爱丽小屋水凝心机液体唇膏OR201 3.5g",\
            "Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g","PriceAndCount": "￥58.0 X 2"}]}
        Result:{u'message': u'下手晚了，您购买的商品中存在已售空的商品', u'result': u'error'}
        '''

        '''
        GoodsInfo: "Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g","PriceAndCount": "￥58.0 X 2"}]}
        Result: {u'message': u'下手晚了，您购买的商品中存在已售空的商品', u'result': u'error'}
        '''
        request_body = urllib.urlencode(dict(GoodsInfo='"Title": "(保税) 爱丽小屋水凝心机液体唇膏OR201 3.5g","PriceAndCount": "￥58.0 X 2"}]}'))
        response = self.fetch(
            "/v1/orders/update", method="POST", body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_update_order(json_data)

    def _check_update_order(self, json_data):
        if json_data:
            print("UpdateOrder:", json_data)


class ApiFindLogisticsHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindLogisticsHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindLogisticsHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_find_logistics(self):
        '''
        OrderId: 31781568013765
        Result: {u'Logistics': [{u'Content': u'订单已支付，正在配货中', u'HandlingTime': None}], u'Waybill': u'', u'CompanyName': u''}
        '''

        '''
        OrderId: None
        Result: {u'message': u'订单号不能为空', u'result': u'error'}
        '''

        '''
        OrderId: Isn't Json data
        Result: {u'message': u'订单号不能为空', u'result': u'error'}
        '''

        '''
        OrderId: 3178156801376523(订单号不存在)
        Result: {u'Logistics': [{u'Content': u'订单已支付，正在配货中', u'HandlingTime': None}], u'Waybill': u'', u'CompanyName': u''}
        '''
        request_body = urllib.urlencode(dict(OrderId='3178156801376523'))
        response = self.fetch(
            "/v1/orders/logistics", method="POST", body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_logistics(json_data)

    def _check_find_logistics(self, json_data):
        if json_data:
            print("FindLogistics", json_data)


class ApiMyOrderDelHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiMyOrderDelHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiMyOrderDelHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_my_order_del(self):
        '''
        id: 20150811169378
        Result: {u'Status': u'1', u'DistributionName': u'支付宝快捷支付', \
            u'DeliverTime': u'全天送货', u'UUID': u'20150811169378', \
            u'DeliverCost': u'￥0', u'CollectPerson': u'41a65b0f7c3d404', \
            u'Price': u'128.0', u'CollectAddress': u'广东省-深圳市-福田区baguailu', \
            u'CollectTel': u'13829572461', u'GoodsList': [{u'PriceAndCount': \
            u'￥128.0 X 1', u'Title': u'3CE保湿遮瑕粉底/BB霜001 30ml', u'GrouponId': \
            u'', u'Price': u'128.0', u'GoodsId': u'177ddb38-cbeb-4a02-bcbc-0fd32a6912b0', \
            u'Abbreviation': u'3CE保湿遮瑕粉底/BB霜00130ml', u'Discount': u'', u'ActivityId': \
            u'', u'GoodsCount': u'1', u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/\
            177ddb38-cbeb-4a02-bcbc-0fd32a6912b0/goods/22547e80-017b-4b6f-bb4c-b999b9a1e25b.JPG'}], \
            u'PayList': [{u'Distribution': u'1', u'DistributionName': u'支付宝快捷支付'}], \
            u'Distribution': u'1', u'GoodsPrice': u'128.0'}
        '''
        '''

        Result: {u'result': u'订单号为空'}
        '''
        '''
        id: 201508111693781
        Result: {u'result': u'订单不存在'}
        '''
        '''
        id: None
        Result: {u'result': u'订单号为空'}
        '''
        '''
        ids: 20150811169378
        Result: {u'result': u'订单号为空'}
        '''
        response = self.fetch(
            "/v1/orders/show?ids=20150811169378", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_mey_order_del(json_data)

    def _check_mey_order_del(self, json_data):
        if json_data:
            print("MyOrderDel", json_data)


class ApiDeleteOrderHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiDeleteOrderHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiDeleteOrderHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_delete_order(self):
        '''
        id: 20150811176226
        Result: DeleteOrder {u'result': u'success'}
        '''
        '''
        id: 201508111762261(订单不存在)
        Result: DeleteOrder {u'result': u'success'}
        '''
        '''
        id: None
        Result: {u'result': u'error'}
        '''
        '''
        Input: no id
        Result: {u'result': u'error'}
        '''
        request_body = urllib.urlencode("")
        response = self.fetch(
            "/v1/orders/delete", method="POST", body=request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_delete_order(json_data)

    def _check_delete_order(self, json_data):
        if json_data:
            print("DeleteOrder", json_data)


# class ApiGetOrderCounthandlerTest(CommonCheck, BaseHTTPTestCase):
#     def setUp(self):
#         super(ApiGetOrderCounthandlerTest, self).setUp()

#     def tearDown(self):
#         super(ApiGetOrderCounthandlerTest, self).tearDown()

#     def get_handlers(self):
#         pass

#     def set_handlers(self):
#         self.app.add_handlers(
#             self.app.settings["api_domain"], handler_api_orders.urls
#         )

#     def test_get_order_count(self):
#         response = self.fetch(
#             "/v1/orders/count", method="GET",
#             headers={"Host":self.app.settings["api_domain"]}
#         )
#         self.assertEqual(response.code, 200)
#         json_data = json.loads(response.body)
#         self._check_get_order_count(json_data)

#     def _check_get_order_count(self, json_data):
#         if json_data:
#             print "GetOrderCount", json_data


class ApiInsertCommentHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiInsertCommentHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiInsertCommentHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_insert_comment(self):
        '''
        Input:?CreatePerson=8&GoodsID=8&Title=8&Content=8&Key1=111,2&Key2=222,3&Key3=333,4&Key4=444,5
        Result: {u'result': u'success'}
        '''
        '''
        Input:?CreatePerson=8&GoodsID=8&Title=8&Content=8&Key1=111,2&Key2=222,3&Key3=333
        Result:{u'result': u'success'}
        '''
        '''
        Input: None
        Result:{u'result': u'error'}
        '''
        '''
        Input:?CreatePerson=8&Title=8&Content=8&Key1=111,2&Key2=222,3
        Result:{u'result': u'success'}
        '''
        '''
        Input:?Title=8&Content=8&Key1=111,2&Key2=222,3&Key3=333,4&Key4=444,5
        Result:{u'result': u'error'}
        '''
        response = self.fetch(
            "/v1/goods_comments/create?Title=8&Content=8&Key1=111,2&Key2=222,3&Key3=333,4&Key4=444,5", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_insert_comment(json_data)

    def _check_insert_comment(self, json_data):
        if json_data:
            print("InsertComment", json_data)


class ApiGatherGoodsListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiGatherGoodsListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiGatherGoodsListHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_gather_goods_list(self):
        '''
        Input: ?=&OrderName=host&PageNum=1&search=%E4%BB%8A%E6%97%A5%E7%83%AD%E5%8D%96&OrderType=ASC
        Result:[{
                "GoodsTitle": "箭牌经典控油洗护套装（洗发水60ml+护发素60ml)",
                "Price": "￥70.0",
                "Abbreviation": "箭牌经典控油洗护套装（洗发水60ml+护发素60ml)",
                "Discount": null,
                "GoodsId": "3b8ecbe3-55b3-4e5c-8727-9a701a4b97e7",
                "ImgView": "http://123.56.109.37:8080/beautalk/localfile/3b8ecbe3-55b3-4e5c-8727-9a701a4b97e7/goods/62c899e3-0100-4aa9-937b-e7c5e6cac5e9.JPG",
                "ForeignPrice": "$9",
                "DomesticPrice": "96"
              },
              ...
            ]
        '''
        '''
        Input: None
        Result:[{
                "GoodsTitle": "雅诗兰黛肌透修护眼部精华霜15ml",
                "Price": "￥420.0",
                "Abbreviation": "雅诗兰黛肌透修护眼部精华霜15ml",
                "Discount": null,
                "GoodsId": "9998225b-4aa2-4d5f-b200-971c32867116",
                "ImgView": "http://123.56.109.37:8080/beautalk/localfile/9998225b-4aa2-4d5f-b200-971c32867116/goods/fc328053-3b86-4878-979b-676824db4da1.JPG",
                "ForeignPrice": "$62.6",
                "DomesticPrice": "560"
              },
              ...
            ]
        '''
        '''
        Input: ?search=%E4%BB%8A%E6%97%A5%E7%83%AD%E5%8D%96
        Result: [{
                "GoodsTitle": "雅诗兰黛肌透修护眼部精华霜15ml",
                "Price": "￥420.0",
                "Abbreviation": "雅诗兰黛肌透修护眼部精华霜15ml",
                "Discount": null,
                "GoodsId": "9998225b-4aa2-4d5f-b200-971c32867116",
                "ImgView": "http://123.56.109.37:8080/beautalk/localfile/9998225b-4aa2-4d5f-b200-971c32867116/goods/fc328053-3b86-4878-979b-676824db4da1.JPG",
                "ForeignPrice": "$62.6",
                "DomesticPrice": "560"
              },
              ...
            ]
        '''
        response = self.fetch(
            "/beautalk/appShopCart/gatherGoodsList.do?search=%E4%BB%8A%E6%97%A5%E7%83%AD%E5%8D%96", method="GET",
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_gather_order_list(json_data)

    def _check_gather_order_list(self, json_data):
        if json_data:
            print("GatherOrderList", json_data)


class ApiInsertIosHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiInsertIosHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiInsertIosHandlerTest, self).tearDown()

    def get_handlers(self):
        # return handler_api_orders.urls
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_orders.urls
    #     )

    def test_api_insert_ios(self):
        '''
        Input:
        Output:{
          "status": "error",
          "message": "订单数据为空",
          "count_change": "0"
        }
        '''
        '''
        Input:{
          "price":"59.0","collect_address":"广东省-深圳市-",
          "login_type":"android","deliver_cost":"0","distribution":"5",
          "goods":[{
            "price_and_count":"59.00X1","goods_title":"MIO 美爱我美爱我集中抗皱面膜 20ml/片*5",
            "stock_count":"10","domestic_price":"159","goods_count":"1","price":"59.00",
            "goods_img_url":"http://123.56.109.37:8080/beautalk/localfile/00535afc-08af-4df2-
            acf8-53c42dda3653/goods/759cbe66-61a7-4ec4-9e3e-9ce0ca444a29.JPG",
            "goods_id":"00535afc-08af-4df2-acf8-53c42dda3653",
            "goods_brief_intro":"MIO 美爱我集中抗皱面膜5片 20ml/片",
            "weight":"20"
          }],
          "deliver_type":"3","collect_tel":"13537777777","collect_person":"klkll"
        }
        Output:{
          "status": "success",
          "private_key": "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAM87N3JGonanv/K0qmlzfp88K2fNPmG2THnXzOGA+TORj64EOiVc7SALwNcUUVbVhY0cJSmk7Jl3O9NA36+ZUG70q1Y+Amtqq3f5yJThBeepF6t3khk4Ex81lHJWMdu1M3So1eQZV/Kb7VoAkGultXmsRTp5vB3bnbHCwCBvhGcPAgMBAAECgYAhIPlbNnmQeH7SIRnBI+qRMEBMJt6bJlaRf/NL9Z9hJBsRGbHl+TYbUmWwvJnIRPhFt8MlJi2A1zPkMNHRs7PMzypaRLA3Dt8VnT9ENQKwZnoeACVj1+65hPEebnUvBnIZNojMO4E+R3xN8VCLU4MuTJR0UJ9npz3VJqSTeBa+iQJBAP2YuHZ9CwfYUAtcKpOpfEoeCQyrUUM3PPLin+mvpj/fOsh6GqWbqMkdZqwLgatw4XlN2U7/Fsljrm4pxvC3a3UCQQDRMgEH/eS+13HQJu/asUt0nIcFJZPzuJbjaLRz/rcRXVL0hEfR3rKIJpWunyQU1xu2FnZ40Dnz0XkFCQrTEevzAkBHQ9Cqs48TAE3WM2tfnaRo67HdVpN6kR5WnysTL6JHlsLdLbspSOoQwmtk88LX29vxC9iCo5rSs2mEWccnRFQ1AkB7rzDk5LxGCWOFSkAt8P1H6PP7mwgq5UxxEAsBOexLG/5cC4nbD+xGi2mcYQMYP0ZnFkjdjV92RLdkvr/jo4j5AkBYEmo6t/CBlxVEuClO9IHWBEMRkTr37xzJMDvCNtyNIg3XUSJo2TbNKJM7rwxk//9ZiY2BO1tK2pEnZwOg8CzV",
          "count_change": "1",
          "order_id": "20151028145702",
          "hgmessage": "customs_place=hangzhou^merchant_customs_code=PT15011301",
          "alipay_account": "2088911062159389",
          "message": "提交成功",
          "distribution": "1"
        }
        '''
        '''
        Input:{
          "price":"59.0","collect_address":"广东省-深圳市-",
          "login_type":"android","deliver_cost":"0","distribution":"5",
          "deliver_type":"3","collect_tel":"13537777777","collect_person":"yuytu"
        }
        Output:{
          "status": "error",
          "message": "订单商品数据为空",
          "count_change": "0"
        }
        '''
        request_body = urllib.urlencode({})
        response = self.fetch(
            "/v1/orders/create", method="POST", body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_api_insert_ios(json_data)

    def _check_api_insert_ios(self, json_data):
        if json_data:
            print("ApiInsertIosHandlerTest:", json_data)


if __name__ == "__main__":
    unittest.main()

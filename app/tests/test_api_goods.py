#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
# import urllib
from urllib import parse as urllib
import unittest
import tornado.testing
import tornado.httpclient

# import meihuishuo.handlers.api.api_goods as handler_api_goods

from app.tests.test_base import BaseHTTPTestCase

class CommonCheck(object):
    pass

class ApiFindGoodsImgListTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindGoodsImgListTest, self).setUp()

    def tearDown(self):
        super(ApiFindGoodsImgListTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_goods.urls
    #     )

    def test_api_find_goods_img_list(self):
        '''
        Input: ?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output:[
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/01c211d1-b76d-4683-85da-5f8fe986bafe.JPG',
            u'ImgType': u'1', u'Resolution': u'1080*389'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/0001a79b-4c35-4b13-aeb7-d5ec400d3044.JPG',
            u'ImgType': u'2', u'Resolution': u'1080*1859'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/51ba7f8b-eb50-4298-9c9a-c0a782659345.JPG',
            u'ImgType': u'2', u'Resolution': u'1080*1476'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/62447db7-db09-40d5-8804-467371ca9c34.JPG',
            u'ImgType': u'2', u'Resolution': u'1080*1470'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/fb2db353-1ce7-4844-b082-8fd2366ca336.JPG',
            u'ImgType': u'2', u'Resolution': u'1080*1864'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/d0cd1974-588f-47b2-95c1-f4d31eb9e9a9.JPG',
            u'ImgType': u'3', u'Resolution': u'1080*1080'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/888cfc04-fa19-4038-8ab7-8eff8f722bc7.JPG',
            u'ImgType': u'3', u'Resolution': u'1080*1080'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/f2d94840-d8db-47e1-ace5-09277878915c.JPG',
            u'ImgType': u'3', u'Resolution': u'1080*1080'},
            {u'ImgView': u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/3dcb5390-a228-4ce2-b332-01c4e09899b8.JPG',
            u'ImgType': u'3', u'Resolution': u'1080*1080'}
            ]
        '''
        '''
        Input: ?GoodsId=
        Output:
        '''
        '''
        Input:
        Output:
        '''
        '''
        Input: ?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a5
        Output:
        '''
        '''
        Input: ?GoodsId=dd789650-aa64-a74aec9ca7a5
        Output:
        '''
        # request_body = urllib.urlencode()
        response = self.fetch(
            "/v1/goods/images?GoodsId=dd789650-aa64-a74aec9ca7a5", method="GET", #body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_goods_img_list(json_data)


    def _check_find_goods_img_list(self, json_data):
        if json_data:
            print("FindGoodsImgList:", json_data)


class ApiFindGoodsDetailListHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindGoodsDetailListHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindGoodsDetailListHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_goods.urls
    #     )

    def test_api_find_goods_detail_list(self):
        '''
        Input: ?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output:[
            {u'Value': u'自然乐园芦荟爽肤水滋润保湿160ml', u'Title': u'商品名称'},
            {u'Value': u'自然乐园', u'Title': u'品         牌'},
            {u'Value': u'160ml/瓶', u'Title': u'产品规格'},
            {u'Value': u'保湿 补水锁水 消炎舒缓 祛痘祛印 美白 防晒 控油', u'Title': u'功         效'},
            {u'Value': u'适合各种肤质，尤其推荐给毛孔粗大的油性、混合性，以及长痘痘的肤质', u'Title': u'适用人群'},
            {u'Value': u'韩国', u'Title': u'原产地区'},
            {u'Value': u'3年（具体日期以收到的实物为准）', u'Title': u'保质期限'}
            ]
        '''
        '''
        Input:
        Output: {"ErrorMsg":u"商品不存在"}
        '''
        '''
        Input: ?GoodsId=?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a5
        Output: {"ErrorMsg":u"商品不存在"}
        '''
        '''
        Input: ?GoodsId=?GoodsId=dd789650-1cc7-49d1-a74aec9ca7a4
        Output: {"ErrorMsg":u"商品不存在"}
        '''
        # request_body = urllib.urlencode()
        response = self.fetch(
            "/v1/goods/specs?GoodsId=None", method="GET", #body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_goods_detail_list(json_data)


    def _check_find_goods_detail_list(self, json_data):
        if json_data:
            print("FindGoodsDetailList:", json_data)


class ApiFindGoodsDetailHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindGoodsDetailHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindGoodsDetailHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_goods.urls
    #     )

    def test_api_find_goods_detail(self):
        '''
        Input: ?MemberId=24f639e9a6644c0&GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output: {
            u'ShareTitle': u'自然乐园芦荟爽肤水滋润保湿160ml', u'GoodsTitle': u'自然乐园芦荟爽肤水滋润保湿160ml',
            u'ShareContent': u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后...', u'Score': u'5.0',
            u'DomesticPrice': u'164', u'Stock': u'60', u'OverseasPrice': u'₩12395', u'Notice': u'0',
            u'Price': u'￥69.0', u'BuyCount': u'762人已购买', u'Discount': u'', u'GoodsIntro':
            u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后温和清新，快速让肌肤喝饱水，无粘稠感，帮助镇静和滋润调理肌肤。',
            u'ActivityName': u'', u'FavorableRate': u'100%', u'Reputation': u'5', u'ActivityTime': u'',
            u'GoodsId': u'dd789650-1cc7-49d1-aa64-a74aec9ca7a4', u'ShareImage':
            u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/3c0d5b3f-3843-4894-a057-f78689f21901.JPG',
            u'HtmlUrl': u'http://app.meihuishuo.com:8080/beautalk/goods/share.do?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4',
            u'Abbreviation': u'自然乐园芦荟爽肤水滋润保湿160ml', u'isCollected': u'NO', u'OriginalPrice': u'￥164'
            }
        '''
        '''
        Input: ?MemberId=24f639e9a6644c0&GoodsId=
        Output: {u'ErrorMsg': u'error'}
        '''
        '''
        Input: ?MemberId=24f639e9a6644c0&GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output: {
            u'ShareTitle': u'自然乐园芦荟爽肤水滋润保湿160ml', u'GoodsTitle': u'自然乐园芦荟爽肤水滋润保湿160ml',
            u'ShareContent': u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后...', u'Score': u'5.0',
            u'DomesticPrice': u'164', u'Stock': u'60', u'OverseasPrice': u'₩12395', u'Notice': u'0', u'Price':
            u'￥69.0', u'BuyCount': u'762人已购买', u'Discount': u'', u'GoodsIntro':
            u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后温和清新，快速让肌肤喝饱水，无粘稠感，帮助镇静和滋润调理肌肤。',
            u'ActivityName': u'', u'FavorableRate': u'100%', u'Reputation': u'5', u'ActivityTime': u'', u'GoodsId':
            u'dd789650-1cc7-49d1-aa64-a74aec9ca7a4', u'ShareImage':
            u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/3c0d5b3f-3843-4894-a057-f78689f21901.JPG',
            u'HtmlUrl': u'http://app.meihuishuo.com:8080/beautalk/goods/share.do?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4',
            u'Abbreviation': u'自然乐园芦荟爽肤水滋润保湿160ml', u'isCollected': u'NO', u'OriginalPrice': u'￥164'
            }
        '''
        '''
        Input: ?MemberId=c0&GoodsId=
        Output: {u'ErrorMsg': u'error'}
        '''
        '''
        Input: ?MemberId=24f639a6644c0&GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output: {u'ErrorMsg': u'error'}
        '''
        '''
        Input: ?MemberId=24f639e9a6644c0&GoodsId=dd789650-49d1-aa64-a74aec9ca7a4
        Output: {u'ErrorMsg': u'error'}
        '''
        '''
        Input:
        Output: {u'ErrorMsg': u'error'}
        '''
        '''
        Input: ?MemberId=&GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output: {
            u'ShareTitle': u'自然乐园芦荟爽肤水滋润保湿160ml', u'GoodsTitle': u'自然乐园芦荟爽肤水滋润保湿160ml',
            u'ShareContent': u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后...', u'Score': u'5.0',
            u'DomesticPrice': u'164', u'Stock': u'60', u'OverseasPrice': u'₩12395', u'Notice': u'0', u'Price':
            u'￥69.0', u'BuyCount': u'762人已购买', u'Discount': u'', u'GoodsIntro':
            u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后温和清新，快速让肌肤喝饱水，无粘稠感，帮助镇静和滋润调理肌肤。',
            u'ActivityName': u'', u'FavorableRate': u'100%', u'Reputation': u'5', u'ActivityTime': u'', u'GoodsId':
            u'dd789650-1cc7-49d1-aa64-a74aec9ca7a4', u'ShareImage':
            u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/3c0d5b3f-3843-4894-a057-f78689f21901.JPG',
            u'HtmlUrl': u'http://app.meihuishuo.com:8080/beautalk/goods/share.do?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4',
            u'Abbreviation': u'自然乐园芦荟爽肤水滋润保湿160ml', u'isCollected': u'NO', u'OriginalPrice': u'￥164'
            }
        '''
        '''
        Input: ?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output: {
            u'ShareTitle': u'自然乐园芦荟爽肤水滋润保湿160ml', u'GoodsTitle': u'自然乐园芦荟爽肤水滋润保湿160ml',
            u'ShareContent': u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后...', u'Score': u'5.0',
            u'DomesticPrice': u'164', u'Stock': u'60', u'OverseasPrice': u'₩12395', u'Notice': u'0', u'Price':
            u'￥69.0', u'BuyCount': u'762人已购买', u'Discount': u'', u'GoodsIntro':
            u'优选有机认证的无公害芦荟，含有丰富的维他命，可以镇静滋润肌肤，用后温和清新，快速让肌肤喝饱水，无粘稠感，帮助镇静和滋润调理肌肤。',
            u'ActivityName': u'', u'FavorableRate': u'100%', u'Reputation': u'5', u'ActivityTime': u'', u'GoodsId':
            u'dd789650-1cc7-49d1-aa64-a74aec9ca7a4', u'ShareImage':
            u'http://123.56.109.37:8080/beautalk/localfile/dd789650-1cc7-49d1-aa64-a74aec9ca7a4/goods/3c0d5b3f-3843-4894-a057-f78689f21901.JPG',
            u'HtmlUrl': u'http://app.meihuishuo.com:8080/beautalk/goods/share.do?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4',
            u'Abbreviation': u'自然乐园芦荟爽肤水滋润保湿160ml', u'isCollected': u'NO', u'OriginalPrice': u'￥164'
            }
        '''
        # request_body = urllib.urlencode()
        response = self.fetch(
            "/v1/goods/show?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4", method="GET", #body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_goods_detail(json_data)


    def _check_find_goods_detail(self, json_data):
        if json_data:
            print("FindGoodsDetail:", json_data)


class ApiFindGoodsScoreHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindGoodsScoreHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindGoodsScoreHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_goods.urls
    #     )

    def test_api_find_goods_score(self):
        '''
        Input: ?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output:[
            {u'Score': u'5.0', u'Title': u'商品质量'},
            {u'Score': u'5.0', u'Title': u'配送速度'},
            {u'Score': u'5.0', u'Title': u'服务质量'},
            {u'Score': u'5.0', u'Title': u'售后服务'}
            ]
        '''
        '''
        Input: ?GoodsId=
        Output:  {u'ErrorMsg': u'error'}
        '''
        '''
        Input:
        Output:  {u'ErrorMsg': u'error'}
        '''
        '''
        Input: ?GoodsId=dd789650-49d1-aa64-a74aec9ca7a4
        Output:[
            {u'Score': u'5.0', u'Title': u'商品质量'},
            {u'Score': u'5.0', u'Title': u'配送速度'},
            {u'Score': u'5.0', u'Title': u'服务质量'},
            {u'Score': u'5.0', u'Title': u'售后服务'}
            ]
        '''
        # request_body = urllib.urlencode()
        response = self.fetch(
            "/v1/goods/score?GoodsId=dd789650-49d1-aa64-a74aec9ca7a4", method="GET", #body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_goods_score(json_data)


    def _check_find_goods_score(self, json_data):
        if json_data:
            print("FindGoodsSorce:", json_data)


class ApiFindGoodsCommentHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindGoodsCommentHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindGoodsCommentHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_goods.urls
    #     )

    def test_api_find_goods_comment(self):
        '''
        Input: ?GoodsId=dd789650-1cc7-49d1-aa64-a74aec9ca7a4
        Output:[
            {u'Content': u'很清爽的水，每天早上拍在脸上，感觉一整天都不会油腻，很适合油性肌肤呢。',
            u'MemberName': u'烟火熏燃814', u'IsEssence': u'2', u'Title': u''},
            {u'Content': u'试了一下芦荟水保湿效果挺好而且不油腻，不错。', u'MemberName':
            u'张张张张总', u'IsEssence': u'2', u'Title': u''},
            {u'Content': u'很保湿，清爽，特别适合夏天使用，不会干，也不油，推荐款。',
            u'MemberName': u'那都不是事儿923', u'IsEssence': u'2', u'Title': u''},
            {u'Content': u'晒后用这款水，有舒缓肌肤的作用，修复的还挺快。', u'MemberName':
            u'翊扬乖乖', u'IsEssence': u'2', u'Title': u''},
            {u'Content': u'自从发现这款爽肤水，就一直在用，效果不错，没有任何不适。',
            u'MemberName': u'judybaby娇', u'IsEssence': u'2', u'Title': u''}
            ]
        '''
        '''
        Input:
        Output:
        '''
        '''
        Input: ?GoodsId=
        Output: {u'ErrorMsg': u'error'}
        '''
        '''
        Input: ?GoodsId=dd789650-1cc7-aa64-a74aec9ca7a4
        Output:
        '''
        # request_body = urllib.urlencode()
        response = self.fetch(
            "/v1/goods/comments?GoodsId=dd789650-1cc7-aa64-a74aec9ca7a4", method="GET", #body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_goods_comment(json_data)


    def _check_find_goods_comment(self, json_data):
        if json_data:
            print("FindGoodsComment:", json_data)


class ApiInsertHandlerHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiInsertHandlerHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiInsertHandlerHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_goods.urls
    #     )

    def test_api_insert(self):
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "dd789650-1cc7-49d1-aa64-a74aec9ca7a4",
            "CollectionType": "2", "MemberId": "24f639e9a6644c0"}')
        Output: {u'result': u'success'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "dd789650-1cc7-49d1-aa64-a74aec9ca7a4",
            "CollectionType": "1", "MemberId": "24f639e9a6644c0"}')
        Output: {u'result': u'success'}
        '''
        '''
        Input: dict(updateCollectionMsg='{}')
        Output: {u'result': u'error'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "dd789650-1cc7-49d1-aa64-a74aec9ca7a4",
            "CollectionType": "1", "MemberId": "24f639e9a6644c0"}')
        Output: {u'result': u'error'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "dd789650-1cc7-49d1-aa64-a74aec9ca7a4",
            "CollectionType": "1", "MemberId": ""}')
        Output: {u'result': u'error'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "dd789650-1cc7-aa64-a74aec9ca7a4",
            "CollectionType": "1", "MemberId": ""}')
        Output: {u'result': u'success'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "",
            "CollectionType": "1", "MemberId": "24f639e9a6644c0"}')
        Output: {u'result': u'success'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "",
            "CollectionType": "1", "MemberId": ""}')
        Output: {u'result': u'error'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "", "RelatedId": "",
            "CollectionType": "", "MemberId": ""}')
        Output: {u'result': u'error'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"MemberId": "24f639e9a6644c0"}')
        Output: {u'result': u'error'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "1", "RelatedId": "",
            "CollectionType": "", "MemberId": "24f639e9a6644c0"}')
        Output: {u'result': u'success'}
        '''
        '''
        Input: dict(updateCollectionMsg='{"RelatedType": "", "RelatedId": "",
            "CollectionType": "1", "MemberId": "24f639e9a6644c0"}')
        Output: {u'result': u'success'}
        '''
        request_body = urllib.urlencode(dict(updateCollectionMsg='{"RelatedType": "", "RelatedId": "","CollectionType": "", "MemberId": "24f639e9a6644c0"}'))
        response = self.fetch(
            "/v1/collections/create", method="POST", body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_insert(json_data)


    def _check_insert(self, json_data):
        if json_data:
            print("Insert:", json_data)


class ApiFindGoodsDetailHandlerTest(CommonCheck, BaseHTTPTestCase):
    def setUp(self):
        super(ApiFindGoodsDetailHandlerTest, self).setUp()

    def tearDown(self):
        super(ApiFindGoodsDetailHandlerTest, self).tearDown()

    def get_handlers(self):
        pass

    # def set_handlers(self):
    #     self.app.add_handlers(
    #         self.app.settings["api_domain"], handler_api_goods.urls
    #     )

    def test_api_find_goods_detail(self):
        '''
        Input:
        Output: {
          "status": "error",
          "message": "没有此商品"
        }
        '''
        '''
        Input:?goods_id=08fc3969-c3eb-455c-aac1-87b28cef3dfb
        Output: {
          "original_price": "208.00",
          "goods_brief_intro": "SNP水库燕窩面膜10片裝",
          "is_favorite": 0,
          "message": "",
          "stock_count": 8,
          "share_content": " 韩国SNP第一药妆的燕窝水库保湿面膜，SNP燕窝补水面膜含有高浓...",
          "score_count": 0,
          "goods_id": "08fc3969-c3eb-455c-aac1-87b28cef3dfb",
          "buy_count": 679,
          "share_url": "http://app.meihuishuo.com:8080/beautalk/goods/share.do?GoodsId=08fc3969-c3eb-455c-aac1-87b28cef3dfb",
          "comment_count": 0,
          "score": "5.0",
          "share_title": "SNP 水库燕窩面膜10片裝",
          "is_sold_out": 0,
          "goods_intro": " 韩国SNP第一药妆的燕窝水库保湿面膜，SNP燕窝补水面膜含有高浓缩燕窝原液，集中供给皮肤水分,锁水能力突出，在皮肤水分子表面形成保护膜防止水分快速流失，令皮肤长时间保湿不缺水,保护修复对外界刺激敏感的皮肤，令其更加健康.",
          "status": "success",
          "price": "135.00",
          "domestic_price": "208.00",
          "share_image": "http://123.56.109.37:8080/beautalk/localfile/08fc3969-c3eb-455c-aac1-87b28cef3dfb/goods/ea87fb06-f904-4241-b766-11053e2aa52b.JPG",
          "high_score_rate": "100%",
          "goods_title": "SNP 水库燕窩面膜10片裝",
          "overseas_price": "₩24419"
        }
        '''
        '''
        Input:?goods_id=08fc3969-c3eb-455c-aac1-87b28cef3df
        Output: {
          "status": "error",
          "message": "没有此商品"
        }
        '''
        '''
        Input:?goods_id=
        Output: {
          "status": "error",
          "message": "没有此商品"
        }
        '''
        # request_body = urllib.urlencode()
        response = self.fetch(
            "/v1/goods/show", method="GET", #body = request_body,
            headers={"Host":self.app.settings["api_domain"]}
        )
        self.assertEqual(response.code, 200)
        json_data = json.loads(response.body)
        self._check_find_goods_detail(json_data)


    def _check_find_goods_detail(self, json_data):
        if json_data:
            print("FindGoodsDetail:", json_data)


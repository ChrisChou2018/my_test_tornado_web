# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import json
# import urllib
# import unittest
# import tornado.testing
# import tornado.httpclient

# # import meihuishuo.handlers.api.api_account as handler_api_account

# # from meihuishuo.tests.test_base import BaseHTTPTestCase

# class CommonCheck(object):
#     pass

# class ApiMemberSigninHandlerTest(CommonCheck, BaseHTTPTestCase):
#     def setUp(self):
#         super(ApiMemberSigninHandlerTest, self).setUp()

#     def tearDown(self):
#         super(ApiMemberSigninHandlerTest, self).tearDown()

#     def get_handlers(self):
#         pass

#     def set_handlers(self):
#         self.app.add_handlers(
#             self.app.settings["api_domain"], handler_api_account.urls
#         )

#     def test_api_member_signin(self):
#         '''
#         Input: dict({'LoginName': u'13829572460', 'Lpassword': u'xzm19920903'})
#         Output: {u'MemberLvl': u'普卡会员', u'ErrorMessage': u'登陆成功', u'MemberId': u'24f639e9a6644c0', u'MemberName': u'zmxu', u'result': u'0'}
#         '''
#         '''
#         Input: {'LoginName': u'13829572460', 'Lpassword': u'xzm19920903'}
#         Output: {u'MemberLvl': u'普卡会员', u'ErrorMessage': u'登陆成功', u'MemberId': u'24f639e9a6644c0', u'MemberName': u'zmxu', u'result': u'0'}
#         '''
#         '''
#         Input: {'LoginName': u'13829572461', 'Lpassword': u'xzm19920903'}
#         Output: {u'MemberLvl': u'', u'ErrorMessage': u'用户不存在', u'MemberId': u'', u'MemberName': u'', u'result': u'error'}
#         '''
#         '''
#         Input: {'Lpassword': u'xzm19920903'}
#         Output: {u'ErrorMessage': u'用户名为空', u'result': u'error'}
#         '''
#         '''
#         Input: {}
#         Output: {u'ErrorMessage': u'用户名为空', u'result': u'error'}
#         '''
#         '''
#         Input: {'LoginName': u'13829572460', 'Lpassword': u'xzm19920902'}
#         Output: {u'MemberLvl': u'', u'ErrorMessage': u'密码错误', u'MemberId': u'', u'MemberName': u'', u'result': u'error'}
#         '''
#         '''
#         Input: ""
#         Output: {u'ErrorMessage': u'用户名为空', u'result': u'error'}
#         '''
#         request_body = urllib.parse.urlencode({'LoginName': u'13829572460', 'Lpassword': u'xzm19920902'})
#         response = self.fetch(
#             "/v1/login", method="POST", body = request_body,
#             headers={"Host":self.app.settings["api_domain"]}
#         )
#         self.assertEqual(response.code, 200)
#         json_data = json.loads(response.body)
#         self._check_member_signin(json_data)


#     def _check_member_signin(self, json_data):
#         if json_data:
#             print("MemberSignin:", json_data)


# class ApiMemberRegistrationHandlerTest(CommonCheck, BaseHTTPTestCase):
#     def setUp(self):
#         super(ApiMemberRegistrationHandlerTest, self).setUp()

#     def tearDown(self):
#         super(ApiMemberRegistrationHandlerTest, self).tearDown()

#     def get_handlers(self):
#         pass

#     def set_handlers(self):
#         self.app.add_handlers(
#             self.app.settings["api_domain"], handler_api_account.urls
#         )

#     def test_api_member_registration(self):
#         '''
#         Input: {'Code': u'266044', 'Telephone': u'13829572460', 'Lpassword': u'xzm19920903'}
#         Output: {u'result': u'SameLoginName'}
#         '''
#         '''
#         Input: {'Code': u'266044', 'Telephone': u'', 'Lpassword': u'xzm19920903'}
#         Output: {u'result': u'codeError'}
#         '''
#         '''
#         Input: {'Code': u'266044', 'Telephone': u'13829572460', 'Lpassword': u''}
#         Output: {u'result': u'SameLoginName'}
#         '''
#         '''
#         Input: {'Code': u'', 'Telephone': u'13829572460', 'Lpassword': u'xzm19920903'}
#         Output: {u'result': u'codeError'}
#         '''
#         '''
#         Input: {'Code': u'175824', 'Telephone': u'13829572470', 'Lpassword': u'xzm19920903'}
#         Output: {u'result': u'codeError'}
#         '''
#         '''
#         Input: {'Code': u'', 'Telephone': u'13829572470', 'Lpassword': u'xzm19920903'}
#         Output: {u'result': u'codeError'}
#         '''
#         '''
#         Input: {'Code': u'175826', 'Telephone': u'13829572470', 'Lpassword': u''}
#         Output: {u'result': u'The password length is less 6'}
#         '''
#         '''
#         Input: {'Code': u'175826', 'Telephone': u'', 'Lpassword': u'xzm19920903'}
#         Output:  {u'result': u'The telephone is None'}
#         '''
#         '''
#         Input: {'Code': u'175826', 'Telephone': u'13829572470', 'Lpassword': u'xzm19920903'}
#         Output: {u'result': u'success'}
#         '''
#         request_body = urllib.parse.urlencode({'Code': u'175826', 'Telephone': u'13829572470', 'Lpassword': u'xzm19920903'})
#         response = self.fetch(
#             "/v1/register", method="POST", body = request_body,
#             headers={"Host":self.app.settings["api_domain"]}
#         )
#         self.assertEqual(response.code, 200)
#         json_data = json.loads(response.body)
#         self._check_member_registration(json_data)


#     def _check_member_registration(self, json_data):
#         if json_data:
#             print("MemberSignin:", json_data)


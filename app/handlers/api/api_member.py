# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import json
# import hashlib
# import tornado.web
# import random
# from datetime import *
# import time
# import uuid
# import sys
# import math

# import bcrypt
# import meihuishuo.libs.picture as lib_picture

# from meihuishuo.libs.handlers import ApiBaseHandler
# from meihuishuo.models.member_model import Member, Opinion, Address
# from meihuishuo.libs.decorators import api_authenticated
# from meihuishuo.models.goods_model import Goods, HomeLimitedGoods, Collection, Country, CurrencyType
# import meihuishuo.models.goods_model as goods_model

# import api_account

# class ApiUpdatePwdHandler(api_account.ApiMemberBase):
#     @api_authenticated
#     def post(self):
#         code = self.get_argument("Code", None)
#         member_id = self.get_argument("MemberId", None)
#         old_password = self.get_argument("OldPass", None)
#         new_password = self.get_argument("NewPass", None)
#         if not member_id:
#             code = self.get_argument("code", None)
#             member_id = self.get_argument("telephone", None)
#             old_password = self.get_argument("old_password", None)
#             new_password = self.get_argument("new_password", None)

#         if self.validate_code(code, member_id) != "success":
#             self.data["status"] = "error"
#             self.data["result"] = "error"
#             if da == "codeError":
#                 self.data["message"] = "验证码错误"
#             elif da == "overtime":
#                 self.data["message"] = "验证超时"
#             elif da == "error":
#                 self.data["message"] = "验证码不存在"
#             self.write(self.data)
#             return

#         new_md5d = hashlib.md5(new_password).hexdigest()
#         new_pass = bcrypt.hashpw(new_md5d, bcrypt.gensalt())
#         old_md5_pass = hashlib.md5(old_password).hexdigest()

#         member_id = self.current_user.member_id
#         member = Member.load_member_by_member_id(member_id)

#         validate_flag = False
#         if member:
#             if (member.hash_pwd and
#                member.hash_pwd == bcrypt.hashpw(old_md5_pass, member.hash_pwd)):
#                 validate_flag = True
#             elif member.password and member.password == old_md5_pass:
#                     validate_flag = True

#         if not validate_flag:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "密码错误"
#             self.write(self.data)
#             return

#         Member.update_pwd(member_id, new_pass)

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiInsertHandler(ApiBaseHandler):
#     # @api_authenticated
#     def post(self):
#         old_key = {"content":"Content", "opinions_type":"OpinionsType",
#             "contact":"Contact"
#         }
#         new_key = {"content":"content", "opinions_type":"opinions_type",
#             "contact":"contact"
#         }
#         key = old_key
#         member_id = self.get_argument("MemberId", "")
#         if not member_id:
#             if self.current_user:
#                 member_id = self.current_user.member_id
#             else:
#                 member_id = ""
#             key = new_key

#         if not self.get_argument(key["content"], ""):
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "反馈的内容不能为空"
#             self.write(self.data)
#             return

#         opinion = Opinion()
#         opinion.title = "无标题"
#         opinion.opinion_id = str(uuid.uuid4())
#         opinion.create_time = datetime.now()
#         opinion.content = self.get_argument(key["content"], "")
#         opinion.opinions_type = self.get_argument(key["opinions_type"], "")
#         opinion.contact = self.get_argument(key["contact"], "")
#         opinion.create_person = member_id
#         opinion.status = "1"
#         opinion.save(force_insert=True)

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiUpdateInfoHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         member_name = self.get_argument("MemberName", None)
#         member_id = self.get_argument("MemberId", None)
#         sex = self.get_argument("Sex", None)
#         birthday = self.get_argument("Birthday", None)
#         if not member_id and not member_name:
#             member_name = self.get_argument("member_name", None)
#             member_id = self.current_user.member_id
#             sex = self.get_argument("sex", None)
#             birthday = self.get_argument("birthday", None)

#         if not member_name or not sex or not birthday:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "请补充完整个人信息"
#             self.write(self.data)
#             return

#         try:
#             member = Member.load_member_by_member_id(member_id)
#         except Exception, e:
#             member = None

#         if not member:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "用户已退出，请重新登录"
#             self.write(self.data)
#             return

#         member.sex = sex
#         member.birthday = birthday
#         member.member_name = member_name
#         member.save()

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiInsertIOShandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         collect_person = self.get_argument("Addressee", None)
#         collect_address = self.get_argument("DetailAddress", None)
#         collect_tel = self.get_argument("Telephone", None)
#         member_id = self.get_argument("MemberId", None)
#         area = self.get_argument("Area", None)
#         if not member_id:
#             member_id = self.current_user.member_id
#             collect_person = self.get_argument("collect_person", None)
#             collect_tel = self.get_argument("collect_tel", None)
#             collect_address = self.get_argument("collect_address", None)
#             area = self.get_argument("area", None)

#         if not member_id and not collect_address and not collect_tel \
#             and not collect_person and not area:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "请补全信息"
#             self.write(self.data)
#             return

#         address = Address()
#         address.addressee = collect_person
#         address.address = collect_address
#         address.telephone = collect_tel
#         address.member_id = member_id
#         address.area = area
#         address.address_id = str(uuid.uuid4())
#         address.create_time = datetime.now()
#         address.update_time = datetime.now()
#         address.save(force_insert=True)

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiFindListHandler(ApiBaseHandler):
#     @api_authenticated
#     def get(self):
#         old_key = {"address_id":"AddressId", "collect_address":"Address",
#             "collect_person":"Addressee", "collect_tel":"Telephone",
#             "area":"Area"
#         }
#         new_key = {"address_id":"address_id", "collect_address":"collect_address",
#             "collect_person":"collect_person", "collect_tel":"collect_tel",
#             "area":"area"
#         }
#         member_id = self.get_argument("MemberId", None)
#         key = old_key
#         if not member_id:
#             member_id = self.current_user.member_id
#             key = new_key

#         if not member_id:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "用户已退出，请重新登录"
#             self.write(self.data)
#             return

#         address = Address.find_all(member_id)

#         result = []
#         for each in address:
#             each_dict = dict()
#             each_dict[key["address_id"]] = each.address_id
#             each_dict[key["collect_address"]] = each.address
#             each_dict[key["collect_person"]] = each.addressee
#             each_dict[key["collect_tel"]] = each.telephone
#             each_dict[key["area"]] = each.area
#             result.append(each_dict)

#         if key["address_id"] == "AddressId":
#             result_data = json.dumps(result)
#             self.set_header("Content-Type", "application/json; charset=UTF-8")
#             self.write(result_data)
#             return

#         self.data["status"] = "success"
#         self.data["addresses"] = result
#         self.write(self.data)


# class ApiDetailHandler(ApiBaseHandler):
#     @api_authenticated
#     def get(self):
#         old_key = {"address_id":"AddressId", "member_id":"MemberId",
#             "collect_person":"Addressee","collect_address":"Address",
#             "collect_tel":"Telephone", "area":"Area", "zip_code":"ZipCode",
#             "create_time":"CreateTime", "update_time":"UpdateTime"
#         }
#         new_key = {"address_id":"address_id", "member_id":"member_id",
#             "collect_person":"collect_person","collect_address":"collect_address",
#             "collect_tel":"collect_tel", "area":"area", "zip_code":"zip_code",
#             "create_time":"create_time", "update_time":"update_time"
#         }
#         key = old_key
#         address_id = self.get_argument("AddressId", None)
#         if not address_id:
#             address_id = self.get_argument("address_id", None)
#             key = new_key

#         if not address_id:
#             self.data["status"] = "error"
#             self.data["message"] = "获取数据出错"
#             self.write(self.data)
#             return

#         address = Address.find_by_id(address_id)
#         if address:
#             self.data[key["address_id"]] = address.address_id
#             self.data[key["member_id"]] = address.member_id
#             self.data[key["collect_person"]] = address.addressee
#             self.data[key["collect_address"]] = address.address
#             self.data[key["collect_tel"]] = address.telephone
#             self.data[key["area"]] = address.area
#             self.data[key["zip_code"]] = address.zip_code
#             self.data[key["create_time"]] = address.create_time.strftime(\
#                 '%Y-%m-%d %H:%M:%S')
#             self.data[key["update_time"]] = address.update_time.strftime(\
#                 '%Y-%m-%d %H:%M:%S')
#             self.data["status"] = "success"
#         self.write(self.data)


# class ApiUpdateIOShandler(ApiBaseHandler):
#     '''
#     线上API没有传MemberId和DetailAddress过来
#     现在需要改成判断MemberId是否为空，为空的话将返回错误信息
#     '''
#     @api_authenticated
#     def post(self):
#         address_id = self.get_argument("AddressId", None)
#         collect_person = self.get_argument("Addressee", None)
#         collect_address = self.get_argument("DetailAddress", None)
#         collect_tel = self.get_argument("Telephone", None)
#         member_id = self.get_argument("MemberId", None)
#         area = self.get_argument("Area", None)

#         if not member_id:
#             address_id = self.get_argument("address_id", None)
#             collect_person = self.get_argument("collect_person", None)
#             collect_address = self.get_argument("collect_address", None)
#             collect_tel = self.get_argument("collect_tel", None)
#             member_id = self.current_user.member_id
#             area = self.get_argument("area", None)

#         if not address_id and not collect_tel and not collect_address \
#             and not collect_person and not area:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "请补全信息"
#             self.write(self.data)
#             return

#         try:
#             address = Address.get(Address.address_id == address_id)
#         except Exception, e:
#             address = None

#         if not address:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "请求出错"
#             self.write(self.data)
#             return

#         address.addressee = collect_person
#         address.address = collect_address
#         address.telephone = collect_tel
#         address.member_id = member_id
#         address.area = area
#         address.update_time = datetime.now()
#         address.save()

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiDeleteHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         address_id = self.get_argument("AddressId", None)
#         if not address_id:
#             address_id = self.get_argument("address_id", None)

#         if not address_id:
#             self.data["result"] = "error"
#             self.data["status"] = "error"
#             self.data["message"] = "网络错误"
#             self.write(self.data)
#             return

#         Address.delete_by_id(address_id)

#         self.data["result"] = "success"
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiMyCollectionListHandler(ApiBaseHandler):
#     @api_authenticated
#     def get(self):
#         member_id = self.current_user.member_id
#         goods = list()

#         goods_ids = [each.related_id for each in Collection.select().where(
#             Collection.member_id == member_id)]
#         if not goods_ids:
#             self.data["status"] = "success"
#             self.data["goods"] = goods
#             self.write(self.data)
#             return

#         goods_list = goods_model.list_goods_min_price(goods_ids)

#         country_list = [each for each in Country.list_countries()]
#         current_type_list = [each for each in CurrencyType.list_currency_type()]

#         for each in goods_list:
#             goods_dict = dict()
#             goods_dict["goods_id"] = each.goods_id
#             goods_dict["goods_img_url"] = self.build_photo_url(each.img_view)
#             goods_dict["buy_count"] = int(each.buy_count)
#             goods_dict["goods_title"] = each.goods_title
#             goods_dict["price"] = str(each.current_price)
#             goods_dict["stock_count"] = int(each.stock)
#             goods_dict["goods_brief_intro"] = each.abbreviation
#             goods_dict["overseas_price"] = str(each.overseas_price)
#             goods_dict["domestic_price"] = str(each.domestic_price)
#             goods_dict["foreign_price"] = str(each.foreign_price)
#             goods_dict["symbol"] = "￥"
#             goods_dict["country_name"] = each.origin
#             goods_dict["country_img_url"] = ""
#             for c_t in current_type_list:
#                 if each.foreign_type == c_t.uuid:
#                     goods_dict["symbol"] = c_t.symbol
#                     break
#             for country in country_list:
#                 if country.country_cn_name in each.origin:
#                     goods_dict["country_name"] = country.country_cn_name
#                     goods_dict["country_img_url"] = self.build_country_img_url(country.country_id)
#                     break
#             goods.append(goods_dict)

#         self.data["goods"] = goods
#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiMemberInfoHandler(ApiBaseHandler):
#     '''
#     Api上没有这个接口
#     查看用户信息时要用到
#     '''
#     @api_authenticated
#     def get(self):
#         old_key = {"member_name":"MemberName", "sex":"Sex", "birthday":"Birthday"}
#         new_key = {"member_name":"member_name", "sex":"sex", "birthday":"birthday"}
#         key = old_key
#         member_id = self.get_argument("MemberId", None)
#         if not member_id:
#             member_id = self.current_user.member_id
#             key = new_key

#         try:
#             member_info = Member.load_member_by_member_id(member_id)
#         except Exception, e:
#             member_info = None

#         if not member_info:
#             self.data["status"] = "error"
#             self.data["message"] = "用户已退出，请重新登录"
#             self.write(self.data)
#             return

#         if member_info.member_name:
#             self.data[key["member_name"]] = member_info.member_name
#         if member_info.sex:
#             self.data[key["sex"]] = member_info.sex
#         if member_info.birthday:
#             self.data[key["birthday"]] = member_info.birthday

#         self.data["status"] = "success"
#         self.write(self.data)


# class ApiUpdateAvatarHandler(ApiBaseHandler):
#     @api_authenticated
#     def post(self):
#         pic_dict = self._upload_photo()
#         if not pic_dict:
#             self.data["message"] = "头像上传失败"
#             self.write(self.data)
#             return

#         self.data["icon_avatar_url"] = self.build_photo_url(
#             pic_dict["picture_id"], "thumb"
#         )
#         self.data["large_avatar_url"] = self.build_photo_url(
#             pic_dict["picture_id"], "hd"
#         )
#         if self.current_user.member_avatar:
#             lib_picture.remove_picture(self.current_user.member_avatar,
#                 self.settings["static_path"], picture_type="avatar"
#             )

#         self.current_user.member_avatar = pic_dict["picture_id"]
#         self.current_user.save()
#         self.data["status"] = "success"
#         self.write(self.data)


# urls = [
#     (r"/v1/account/update_password", ApiUpdatePwdHandler),

#     (r"/v1/feedbacks/create", ApiInsertHandler),

#     (r"/v1/account/update_profile", ApiUpdateInfoHandler),

#     (r"/v1/account/addresses/create", ApiInsertIOShandler),

#     (r"/v1/account/addresses", ApiFindListHandler),

#     (r"/v1/account/addresses/show", ApiDetailHandler),

#     (r"/v1/account/addresses/update", ApiUpdateIOShandler),

#     (r"/v1/account/addresses/destroy", ApiDeleteHandler),

#     (r"/v1/collections/", ApiMyCollectionListHandler),

#     (r"/v1/account_base_info", ApiMemberInfoHandler),

#     (r"/v1/update_avatar", ApiUpdateAvatarHandler),
# ]

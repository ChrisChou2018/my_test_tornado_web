#Ubskin API & Admin Site
##Configuration notes
推荐使用 Nginx 作为本地 Web 服务器。
复制 conf/vhost_dev.conf 为 conf/vhost_dev_xxx.conf，xxx 建议为用户名。
注意修改nginx配置文件中的静态文件地址
```
root /Users/matt/Projects/ubskin_web/assets;
```
和
```
root /Users/matt/Projects/backup/ubskin/static;
```

然后在 Nginx 配置文件中导入该文件即可：
```
include /Users/matt/Projects/ubskin_web/conf/vhost_dev.conf;
```

##Development notes
配置文件（涉及到路径、本机配置相关，都在这里设置，不要直接修改 config_web.py）：
请在根目录创建 config_local.py，内容如下：
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ["STATIC_PATH"] = "/path/to/ubskin/static/"
```


HOST:
```
127.0.0.1       ubs_db
127.0.0.1       www-local.ubskin.net
127.0.0.1       s-local.ubskin.net
127.0.0.1       api-local.ubskin.net
127.0.0.1       admin-local.ubskin.net
127.0.0.1       m-local.ubskin.net
```
####初始化数据表
```cdm
python3 do_work.py init_table
```

##用户部分的接口(API)
###会员注册
* URL: http://api-local.ubskin.net/v1/register/
method: POST
传入数据
注册手机号：telephone
密码 ：password
######返回参数：Dict
* 成功标识：status 【error 为登陆失败；success 为登陆成功；】
* 返回信息：message
* 用户名：member_name
* 用户ID：member_id
* session_id：session_id
<font color="red"> 登录成功后，在其它接口，member_id和session_id和被封装在HTTP请求Header的Authorization中。格式为：Authorization : member_id:session_id </font>
```python
{
    "status": "success",
    "message": "",
    "member_name": "UBS_16085410",
    "member_id": 4,
    "session_id": "qt56yxwrfy"
}
```
###会员登录
* URL: http://api-local.ubskin.net/v1/signin/
method: POST
传入数据
注册手机号：telephone
密码 ：password

######返回参数：Dict
* 成功标识：status 【error 为登陆失败；success 为登陆成功；】
* 返回信息：message
* 用户名：member_name
* 用户ID：member_id
* session_id：session_id
<font color="red"> 登录成功后，在其它接口，member_id和session_id和被封装在HTTP请求Header的Authorization中。格式为：Authorization : member_id:session_id </font>
```python
{
    "status": "success",
    "message": "",
    "member_name": "UBS_16085410",
    "member_id": 4,
    "session_id": "qt56yxwrfy"
}
```

###更改密码

####1）步骤一，验证旧密码

* URL: http://api-local.ubskin.net/v1/change_password_step1/
method: POST
传入数据：
	* 旧密码：password
	
######返回参数：Dict
* 成功标识：status 【error 为失败携带错误信息message；success 为验证成功；】
* 返回信息：message
```
{
    "status": "success",
    "message": ""
}
```

####2）步骤二，设置新密码

* URL:http://api-local.ubskin.net/v1/change_password_step2/
method:POST
传入数据：
	* 新密码：password

######返回参数：Dict
* 成功标识：status 【error 为失败，携带错误信息message；success 为设置成功；】
* 返回信息：message
```
{
    "status": "success",
    "message": ""
}
```

##商品信息部分的接口(API)

###获取所有商品信息

* URL： http://api-local.ubskin.net/v1/get_items/
method：GET
传入数据：
	* 第几页：page

######返回参数：Dict
* 成功标示：status
* 返回信息：message
* 商品数据：data（list）
```
{
    "status": "success",
    "message": "",
    "data": [
        {
            "item_id": 3,
            "item_name": "大宝SD蜜",
            "item_info": null,
            "item_code": null,
            "item_barcode": null,
            "price": null,
            "current_price": null,
            "foreign_price": null,
            "comment_count": null,
            "hot_value": null,
            "buy_count": null,
            "key_word": null,
            "origin": null,
            "shelf_life": null,
            "capacity": null,
            "specifications_type_id": 0,
            "categories_id": 3,
            "brand_id": null,
            "for_people": null,
            "weight": null,
            "create_person": "chris",
            "create_time": 1528428085,
            "update_person": "chris",
            "update_time": 1528428120,
            "status": "normal",
            "image_list": []
        }
    ]
}
```

###获取商品分类

* URL：http://api-local.ubskin.net/v1/get_categories/
method：GET

######返回参数：Dict
* 成功标示：status
* 返回信息：message
* 分类数据：data（list）
```
{
    "status": "success",
    "message": "",
    "data": [
        {
            "功效专区": [
                {
                    "categorie_id": 2,
                    "categorie_name": "美白",
                    "categorie_type": 0,
                    "image_path": null
                },
                {
                    "categorie_id": 3,
                    "categorie_name": "护肤",
                    "categorie_type": 0,
                    "image_path": null
                }
            ]
        },
        {
            "基础护理": [
                {
                    "categorie_id": 4,
                    "categorie_name": "祛痘",
                    "categorie_type": 1,
                    "image_path": null
                }
            ]
        },
        {
            "个性彩妆": []
        },
        {
            "营养保健": []
        }
    ]
}
```

###筛选商品信息

* URL：http://api-local.ubskin.net/v1/filter_item/
method：GET
传入参数
	* 分类ID：categorie_id

######返回参数：Dict
* 成功标示：status
* 返回信息：message
* 商品数据：data（list）

```
{
    "status": "success",
    "message": "",
    "data": [
        {
            "item_id": 3,
            "item_name": "大宝SD蜜",
            "item_info": null,
            "item_code": null,
            "item_barcode": null,
            "price": null,
            "current_price": null,
            "foreign_price": null,
            "comment_count": null,
            "hot_value": null,
            "buy_count": null,
            "key_word": null,
            "origin": null,
            "shelf_life": null,
            "capacity": null,
            "specifications_type_id": 0,
            "categories_id": 3,
            "brand_id": null,
            "for_people": null,
            "weight": null,
            "create_person": "chris",
            "create_time": 1528428085,
            "update_person": "chris",
            "update_time": 1528428120,
            "status": "normal",
            "image_list": []
        }
    ]
}
```

###提交评论

* URL：http://api-local.ubskin.net/v1/create_comment/
method：POST
传入参数
	* 用户ID：member_id
	* 商品ID：item_id
	* 评论内容： item_id
	* 评论图片：{'image_name': image_file_obj}

######返回参数：Dict
* 成功标示：status
* 返回信息：message
```
{
    "status": "success",
    "message": ""
}
```



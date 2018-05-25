#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import peewee

try:
    import config_local
except:
    pass


site_name = "优贝施"

base_dir = os.path.dirname(os.path.abspath(__file__))

# search index path
index_path = os.path.join(base_dir, "..", "index_data")

db_host = os.getenv("DB_HOST", "ubs_db")
# db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "ubskin_web")
db_port = os.getenv("DB_PORT", "3306")
db_user = os.getenv("DB_USER", "dev")
db_pass = os.getenv("DB_PASS", "devPass")

# 限时抢购时间段配置
# 请注意按时间顺序进行排序
limit_duration_list = [
    {"start": "00:00:00", "end": "00:00:00"},
    {"start": "10:00:00", "end": "00:00:00"},
    {"start": "15:00:00", "end": "00:00:00"},
    {"start": "20:00:00", "end": "00:00:00"},
]


redis_host = "127.0.0.1"
redis_port = "6379"

# secret = "ubskin123456"


settings_common = {
    "static_version": "1.0.2",
    "app_base_path": base_dir,
    "template_path": os.path.join(base_dir, "app", "templates"),
    "login_url": "/signin",
    "site_name": site_name,
    "xsrf_cookies": True,
    "cookie_secret": "11oETkKXQAGaYdkL5gEmGeJkFuYh7EQnp2XdTP1o/Vo=",
    "cookie_key_sess": "ubsc1",
    # "ui_modules": ui_modules,
    #"gzip": True
    "static_path": os.getenv("STATIC_PATH", os.path.join(base_dir, "..", "static")),
    "cdn_domain": "http://ubs-static-goods.b0.upaiyun.com/",
    "cdn_assets_domain": "http://ubs-assets.b0.upaiyun.com",

    "redis_expire_duration": 60 * 60,
    "redis_on": True,

    "debug": True,
}

settings_debug = {
    "m_domain": "m-local.ubskin.net",
    "www_domain": "www-local.ubskin.net",
    "api_domain": "api-local.ubskin.net",
    "stat_domain": "stat-local.ubskin.net",
    "admin_domain": "admin-local.ubskin.net",
    # "static_domain": "http://slocal.ubskin.net:8080/",
    "m_domain_path": "http://m-local.ubskin.net:8080/",
    "static_domain": "http://s.ubskin.net/",
    "redis_on": True if os.getenv("REDIS_ON") == "True" else False,
}   

settings_testing = {
    "m_domain": "mtest.ubskin.net",
    "www_domain": "wwwtest.ubskin.net",
    "api_domain": "apitest.ubskin.net",
    "stat_domain": "stattest.ubskin.net",
    "admin_domain": "admintest.ubskin.net",
    "m_domain_path": "http://mtest.ubskin.net/",
    "static_domain": "http://s.ubskin.net/",
    "redis_on": False,
}

settings_online = {
    "m_domain": "m.ubskin.net",
    "www_domain": "www.ubskin.net",
    "api_domain": "api.ubskin.net",
    "stat_domain": "stat.ubskin.net",
    "admin_domain": "admin.ubskin.net",
    "m_domain_path": "http://m.ubskin.net/",
    "static_domain": "http://s.ubskin.net/",
    "static_path": os.path.join(base_dir, "..", "static"),
    "debug": False,
}


settings_common["running_status"] = os.getenv("RUNNING_STATUS", "debug")

if settings_common["running_status"] == "debug":
    settings_common.update(settings_debug)
elif settings_common["running_status"] == "testing":
    settings_common.update(settings_testing)
elif settings_common["running_status"] == "online":
    settings_common.update(settings_online)
settings = settings_common


# db = peewee.MySQLDatabase(db_name, user=db_user, password=db_password,
#     host=db_host, port=db_port
# )


# search server
search_url = "http://localhost:8000/SEARCH_RPC"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import hashlib
import urllib2
import json
import random
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import meihuishuo.models.util_model as util_model
import config_web
import meihuishuo.libs.data as lib_data
import datetime as dt
import time

def random_str(r_len=32):
    seed = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join([each for each in random.sample(seed, r_len)])

def xml_to_dict(xml_str):
    root = ET.fromstring(xml_str)
    res_dict = dict()
    for child in root:
        res_dict[child.tag] = child.text

    return res_dict

def dict_to_xml(base_data):
    imp = xml.dom.minidom.getDOMImplementation()
    dom = imp.createDocument(None, 'xml', None)

    root = dom.documentElement
    ks = base_data.keys()
    ks.sort()
    for key in ks:
        if key != "sign":
            item = dom.createElement(key)
            text = dom.createTextNode(base_data[key])
            item.appendChild(text)
            root.appendChild(item)

    if "sign" in ks:
        item = dom.createElement("sign")
        text = dom.createTextNode(base_data["sign"])
        item.appendChild(text)
        root.appendChild(item)

    return root.toprettyxml(encoding="utf-8")


def static_convert_cdn(static_url):
    """将原来的静态服务器图片地址转换为cdn地址

    :param static_url:原来的图片服务器地址
    :return: 对应的cdn服务器地址
    """
    img_match = re.match(r"http:\/\/s\.meihuishuo\.com\/photos\/(?P<pic_version>.*?)"
                    r"\/.*?\/(?P<photo_id>.*?)\.jpg", static_url)
    if not img_match:
        return img_match

    img_info = img_match.groupdict()
    cdn_url = build_photo_url(img_info["photo_id"], pic_version=img_info["pic_version"],
                              pic_type="goods", cdn=True)

    return cdn_url


def replace_img_to_cdn(html):
    """替换发现文章中的图片地址

    首先采用正则进行获取相关的地址,然后进行替换
    """

    goods_imgs = re.findall(r"http:\/\/s\.meihuishuo\.com\/photos\/"
                            r".*?\/.*?\/.*?\.jpg", html)

    if not goods_imgs:
        return html

    # 提取相应的图片 id 和格式，并进行替换
    for img_url in goods_imgs:
        cdn_url = static_convert_cdn(img_url)
        html = html.replace(img_url, cdn_url)

    return html


def str_to_html(strings, term_type):
    goods = re.findall(r"%---.*?---%", strings)
    if not goods:
        return replace_img_to_cdn(strings)

    proto = "http://meihuishuo.com/goods/"
    # if term_type == "app":
    #     proto = "mhs://goods/"
    if term_type == "mobile":
        proto = "http://m.meihuishuo.com/goods/"

    for each in goods:
        s_l = each.split("@")
        img_url = build_photo_url(s_l[2], pic_version="smdl", pic_type="goods", cdn=True)
        goods_id = s_l[0].strip("%---")
        html = "".join(['<div class="goods-item"><a href="'+ proto + goods_id + '">',
                        '<span><span style="float:left;">',
                        '<img class="goods-img" src="', img_url, '"></span>',
                        '<span class="item-content">',
                        '<span class="title" href="',proto, goods_id, '">', s_l[1],
                        '</span><div class="describe">', s_l[3], '</div>',
                        '<span class="price">￥', s_l[4].replace("---%", ""),
                        '</span></span></a></div>'])
        strings = strings.replace(each, html)

    return replace_img_to_cdn(strings)


def deal_article_goods(content, article_id, title, status="new"):
    ags = list()
    a_goods = list()
    goods = re.findall(r"%---.*?---%", content)

    if status != "new":
        a_goods = util_model.ArticleGoods.list_goods_by_article_id(article_id)

    for each in goods:
        is_has = False
        s_l = each.split("@")
        ag_dict = dict()
        for ag in a_goods:
            if ag.goods_id == s_l[0].replace("%---", ""):
                is_has = True
                if ag.article_title != title:
                    util_model.ArticleGoods.update_article_goods(article_id,
                        ag.goods_id, {"article_title": title}
                    )
                a_goods.remove(ag)
                break

        if not is_has:
            ag_dict["goods_id"] = s_l[0].replace("%---", "")
            ag_dict["article_id"] = article_id
            ag_dict["article_title"] = title
            ags.append(ag_dict)

    for each in a_goods:
        util_model.ArticleGoods.update_article_goods(article_id,
            each.goods_id, {"status": "deleted"}
        )

    if ags:
        util_model.ArticleGoods.insert_many_article_goods(ags)


def build_photo_url(photo_id, pic_version="title", pic_type="photos", cdn=False):
    identifier = "!"
    if not cdn:
        if photo_id:
            if "/" in photo_id:
                return photo_id
            else:
                if ".jpg" in photo_id:
                    return "".join([config_web.settings["static_domain"], pic_type,
                        "/", pic_version, "/",photo_id[:2] ,"/", photo_id]
                    )
                else:
                    return "".join([config_web.settings["static_domain"], pic_type,
                        "/", pic_version, "/",photo_id[:2] ,"/", photo_id, ".jpg"]
                    )
        else:
            return "".join(["/images/", "pic_none_", pic_type, ".png"])
    else:
        if photo_id:
            if "/" in photo_id:
                return photo_id
            else:
                if ".jpg" in photo_id:
                    return "".join([config_web.settings["cdn_domain"], pic_type,
                                    "/", photo_id, identifier , pic_version])
                else:
                    return "".join([config_web.settings["cdn_domain"], pic_type,
                                    "/", photo_id, ".jpg", identifier , pic_version])
        else:
            return "".join(["/images/", "pic_none_", pic_type, ".png"])


def build_country_img_url(img_name):
    """构建国家图标url"""
    if not img_name:
        return None
    else:
        return "http://s.meihuishuo.com/images/country/"+img_name+".png"


def build_apk_url(file_name):
    if not file_name:
        return None
    else:
        return config_web.settings["static_domain"]+"files/apk/"+file_name


def build_assets_url(filename, image):
    """构建静态文件url"""

    # 根据运行模式生成相应的 url
    if image:
        if not config_web.settings["debug"]:
            return "".join([config_web.settings["cdn_assets_domain"], filename])
        else:
            return filename

    if not config_web.settings["debug"] and filename in lib_data.assets_dict:
        return "".join([config_web.settings["cdn_assets_domain"],
                        lib_data.assets_dict[filename]])
    else:
        return filename


def mk_filename(filename):
    """获取相应带有时间戳的文件名

    :param filename: 文件名
    :return: 带有时间戳的文件名
    """
    # path_to_file = "/".join([config_web.base_dir, "assets", filename.lstrip("/")])
    mtime = hashlib.md5(str(os.stat(filename).st_mtime)).hexdigest()

    path = ""
    if "/" in filename:
        path, filename = filename.rsplit("/", 1)

    name, suffix = filename.rsplit(".", 1)

    if not path:
        return "".join([name, "-", str(mtime), '.', suffix])
    else:
        return os.path.join(path, "".join([name, "-", str(mtime), '.', suffix]))


def assets_map():
    """得到新的文件名以及对应的文件"""
    root = os.path.join(config_web.base_dir, "assets")

    for parent, _, filenames in os.walk(root):

        for filename in filenames:
            path_to_file = os.path.join(parent, filename)
            original_file = path_to_file.split(root)[-1]

            newfile = mk_filename(path_to_file)  # 获取相应带有时间戳的文件名
            des_file = newfile.split(root)[-1]

            lib_data.assets_dict[original_file] = des_file  # 加入到对应关系


def post(url, data={}):
    flag_count = 0
    while True:
        flag_count += 1
        try:
            req = urllib2.Request(url=url, data=json.dumps(data))
            req.add_header('Content-Type', 'application/json')
            res_data = urllib2.urlopen(req)
            return json.loads(res_data.read())
        except Exception, e:
            if flag_count > 5:
                return ""
            continue


def delay_time(day=1, hour=9, minute=0, second=0):
    # calc seconds to next day 9:00am
    tomo_am = dt.datetime.replace(dt.datetime.utcnow() + dt.timedelta(days=day),
                                  hour=hour, minute=minute, second=second)
    return tomo_am - dt.datetime.now()


def save_upload_excel(excel_file, base_static_path, file_name=""):
    file_name = file_name+str(int(time.time()))+".xls"
    d_path_raw = os.path.join(base_static_path, "files", "excel")
    f_path_raw = os.path.join(d_path_raw, file_name)
    if not os.path.exists(d_path_raw):
        os.makedirs(d_path_raw, 0755)

    with open(f_path_raw, "wb") as f:
        f.write(excel_file)

    return f_path_raw


def timestamp2str(timestamp):
    return dt.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

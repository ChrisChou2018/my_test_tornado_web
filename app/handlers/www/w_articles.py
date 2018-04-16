# -*- coding: utf-8 -*-

import math
import re
import time

import meihuishuo.models.util_model as util_model
from meihuishuo.libs.handlers import WwwBaseHandler
from meihuishuo.libs.pagination import Paginator


class WwwArticleDetailHandler(WwwBaseHandler):
    def get(self, article_id):
        category_list = self.get_category()
        article = util_model.Articles.load_article_by_article_id(article_id,
                                                                 article_status="on")

        recent_articles = self._get_recent_explore()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(article.create_at))
        try:
            pic_url = self.build_photo_url(article.pic_id+'.jpg', pic_version='hd',
                                           pic_type="goods", cdn=True)
        except:
            pic_url = ""

        self.render("www/w_article.html",
                    category_list=category_list, article=article,
                    recent_articles=recent_articles, create_time=create_time,
                    pic_url=pic_url)

    def _get_recent_explore(self):
        recent_articles = util_model.Articles.list_articles(start=0,num=5,
                                                            article_status="on")

        articles = []
        for item in recent_articles:
            article  = {}
            article["article_id"] = item.article_id
            article["title"] = item.title
            article["pic_url"] = self.build_photo_url(item.pic_id, pic_version="thumb",
                                                      pic_type="goods", cdn=True)

            articles.append(article)

        return articles


class WwwExploreHandler(WwwBaseHandler):
    def get(self):
        category_list = self.get_category()
        num_of_page = 30
        page_num = self.get_argument("page_num", "1")
        if page_num.isdigit():
            page_num = int(page_num)
        else:
            page_num = 1

        count = util_model.Articles.list_articles(is_count=True, article_status="on")
        if int(math.ceil(count/num_of_page)) < page_num:
            page_num = 1

        article_l = util_model.Articles.list_articles(start=(page_num-1)*num_of_page,
                                                      num=num_of_page, article_status="on")

        articles = []
        for item in article_l:
            article  = {}
            article["article_id"] = item.article_id
            article["title"] = item.title
            content = re.sub("(\<.*?\>)*(\&.*?\;)*", "", item.content)
            article["content"] = content[:120]
            article["pic_url"] = self.build_photo_url(item.pic_id, pic_version='title',
                                                      pic_type="goods", cdn=True)

            articles.append(article)

        paginator = Paginator(count, num_of_page)
        page = paginator.page(page_num)
        pages = paginator.calculate_display_pages(page)
        page_num = paginator.total_pages
        less_than_certain_size = paginator.check_less_than_certain_size()
        page_args = {"page": page, "pages": pages,
                     "less_than_certain_size": less_than_certain_size,
                     "current_page": page_num,
                     "page_num": page_num}

        self.render("www/w_explore.html",
                    category_list=category_list, articles=articles,
                    page_args=page_args)


urls = [
    (r"/articles/([a-z0-9-]+)/?", WwwArticleDetailHandler),
    (r"/explore/?", WwwExploreHandler),
]

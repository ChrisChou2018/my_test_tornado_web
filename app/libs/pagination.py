#!/usr/bin/env python
# coding:utf-8

import math


class InvalidPage(Exception):pass


class PageNotAnInteger(InvalidPage):pass


class EmptyPage(InvalidPage):pass


class Paginator(object):
    #
    # 用于分页处理的类
    #

    def __init__(self,
                 total_records=None,
                 per_page=None,
                 display_certain_size=5):
        # 总记录数
        self.total_records = total_records
        # 每页显示的条数
        self.per_page = per_page
        # 总页数
        self.total_pages = 0
        # 当前显示的页码数
        self.display_certain_size = display_certain_size
        # 计算出来的数据
        self.data = {}
        #开始计算分页
        self.__judge__()

    def __judge__(self):
        # 如果总记录不够在一页显示，则开始分页
        if self.total_records > self.per_page:
            # 计算总页数 向下取整
            self.total_pages = int(math.ceil(self.total_records/float(self.per_page)))
            # 计算每页的起始和结束位置即[start:end]
            for i in range(0, self.total_pages):
                if i == 0:
                    self.data[i+1] = Page(i+1, i, i+self.per_page, self)
                else:
                    self.data[i+1] = Page(i+1, self.data[i].end,
                                          self.data[i].end + self.per_page,
                                          self)

            # 如果计算出来的页数不恰巧是个整数，那么还需要计算最后一页
            if self.total_pages < (self.total_records/float(self.per_page)):
                # 计算最后一页,因为最后一页肯定是能全页显示的
                self.data[self.total_pages+1] = Page(self.total_pages+1,
                                                     self.data[self.total_pages].end,
                                                     self.total_records,
                                                     self)
        else:
            self.total_pages = 1
            self.data[1] = Page(1, 0, self.total_records, self)

    # 根据页码，返回每页数据的开始和结束位置
    def page(self, page_number):
        page_number = int(page_number)
        if page_number in self.data.keys():
            return self.data[page_number]
        else:
            raise EmptyPage("the page contains no results")

    # 判断是否总页数少于一次性显示的页数，这个主要是可以自己定制页
    # 面的链接数的显示，比如如果为true，那么下一页和上一页就可以不显示
    def check_less_than_certain_size(self):
        if len(self.data) <= self.display_certain_size:
            return True
        else:
            return False

    # 根据计算每次需要显示的页面链接数,即如果
    # 当前是:2,3,4,5 当点击4时,页面的显示应该怎样显示
    def calculate_display_pages(self, page_number):
        #如果当前请求的页面数小于每次显示的链接数
        display_pages = {}
        #全部链接都显示，如果只有一页不显示链接数
        if len(self.data) == 1:
            display_pages[0] = self.data[1]
            # return None
        elif self.check_less_than_certain_size():
            return self.sort_dict_values(self.data)
        else:
            if page_number <= self.display_certain_size/float(2):
                for i in range(0, self.display_certain_size):
                    display_pages[i+1] = self.data[i+1]
            else:
                #当前页面减去显示大小的一半 还大于0，加上显示大小的一半还小于总的大小
                half_of_display_certain_size = int(math.floor(self.display_certain_size/float(2)))
                if page_number-half_of_display_certain_size > 0 and \
                    page_number + half_of_display_certain_size <= len(self.data):
                    for i in range(page_number - half_of_display_certain_size, page_number + half_of_display_certain_size + 1):
                        display_pages[i] = self.data[i]
                else:
                    for i in range(len(self.data) - self.display_certain_size + 1, len(self.data) + 1):
                        display_pages[i] = self.data[i]

        return self.sort_dict_values(display_pages)

    # 因为字典是无序的，先进行排序
    def sort_dict_values(self, adict):
        keys = adict.keys()
        keys.sort()

        return [(key, adict[key]) for key in keys]


#页面类 包含每页取数的开始和结束位置，以及页面的位置
class Page(object):

    def __init__(self, page_number=1, start=0, end=0, paginator=None):
        #每页的起始位置
        self.start = start
        #每页的结束位置
        self.end = end
        #每页的页码
        self.page_number = page_number
        #分页工具类
        self.paginator = paginator
        #下一页
        self.next_page_number = self.page_number+1
        #上一页
        self.prev_page_number = self.page_number-1

    def __repr__(self):
        return '<Page start at %s end at %s>' % (self.start, self.end)

    #是否具有下一页
    def has_next(self):
        # math.ceil(self.paginator.total_records/float(self.paginator.per_page))
        return self.page_number < self.paginator.total_pages

    #是否有前一页
    def has_prev(self):
        return self.page_number > 1

# coding:utf-8

from meihuishuo.libs.handlers import WwwBaseHandler

class FooterHandler(WwwBaseHandler):
    """针对网站底部页面对应的请求
    """
    def get(self, el):
        category_list = self.get_category()
        #
        # title: 一级目录
        # content_title: 二级目录
        # content: 相应目录下面的文字
        #
        if not el:
            title = ""
            content_title = ""

        elif el == "support":
            title = "美会说保障"
            content_title = "自营正品"
        elif el == "directmail":
            title = "美会说保障"
            content_title = "海外直邮"

        elif el == "buy":
            title = "新手指南"
            content_title = "购物流程"
        elif el == "epay":
            title = "新手指南"
            content_title = "支付方式"
        elif el == "coupon":
            title = "新手指南"
            content_title = "优惠券说明"
        elif el == "faq":
            title = "新手指南"
            content_title = "常见问题"

        # elif el == "returnpolicy":
        #     title = "售后服务"
        #     content_title = "退货政策"

        elif el == "cancelorder":
            title = "售后服务"
            content_title = "取消订单"
        elif el == "returnprocess":
            title = "售后服务"
            content_title = "退款流程"
        elif el == "refund":
            title = "售后服务"
            content_title = "退款说明"

        elif el == "deliverymode":
            title = "物流配送"
            content_title = "配送方式"
        elif el == "freight":
            title = "物流配送"
            content_title = "运费标准"
        elif el == "logistracking":
            title = "物流配送"
            content_title = "物流跟踪"

        elif el == "siteintro":
            title = "关于我们"
            content_title = "网站简介"
        elif el == "contactus":
            title = "关于我们"
            content_title = "联系我们"
        else:
            title = None
            content_title = None

        self.render("www/w_footer_content.html",
                    category_list=category_list, title=title,
                    el=el, content_title=content_title)

urls = [
    (r"/footer/([a-z]+)/?", FooterHandler),
]

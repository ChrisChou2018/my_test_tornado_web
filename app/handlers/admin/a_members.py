#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import tornado.web

import app.models.member_model as member_model
import app.models.coupon_model as coupon_model

from app.libs.handlers import SiteBaseHandler, JsSiteBaseHandler
from app.libs.decorators import has_permission
from app.models.member_model import Member
from app.models.order_model import Order
from app.models.goods_model import Comment


class AdminMembersHandler(SiteBaseHandler):
    @tornado.web.addslash
    @has_permission("member")
    def get(self):
        member_id = self.get_argument("member_id", "")
        telephone = self.get_argument("telephone", "")
        is_staff = self.get_argument("is_staff", "")
        if is_staff == "Y":
            is_staff = True
        elif is_staff == "N":
            is_staff = False
        else:
            is_staff = None
        vip_only = self.get_argument("vip_only", "")
        is_vip = True if vip_only == "Y" else False
        member_count = Member.list_members(
            is_count=True, member_id=member_id, telephone=telephone, is_staff=is_staff,
            is_vip=is_vip
        )
        members = [each for each in Member.list_members(
            start=self.start, num=50, member_id=member_id, telephone=telephone,
            is_staff=is_staff, is_vip=is_vip)
        ]
        self.render(
            "a_members/a_members.html", member_id=member_id,
            telephone=telephone, num=50, members=members,
            is_staff=is_staff, member_count=member_count
        )


# /member/detail/xxx
class AdminMemberDetailHandler(SiteBaseHandler):
    @tornado.web.addslash
    @has_permission("member")
    def get(self, member_id):
        member = Member.load_member_by_member_id(member_id)
        if not member:
            self.send_error(404)
            return

        vip_avail = "从未成为 VIP"
        localtime = time.localtime(member.vip_avail_at)
        if member.vip_avail_at > int(time.time()):
            vip_avail = "将于 " + time.strftime("%Y-%m-%d", localtime) + " 到期"
        elif member.vip_avail_at > 0:
            vip_avail = "已于 " + time.strftime("%Y-%m-%d", localtime) + " 到期"

        acc_logs = member_model.list_account_balance_logs(member_id)
        orders = [each for each in Order.get_my_order(member_id, status="0")]
        comments = Comment.list_comments_by_member_id(member_id)

        self.render(
            "a_members/a_member_detail.html", acc_logs=acc_logs, orders=orders,
            member=member, comments=comments, vip_avail=vip_avail
        )


# /members/vips/
class AdminMemberVipsHandler(SiteBaseHandler):
    """Member Vips
    """
    @tornado.web.addslash
    @has_permission("member")
    def get(self):
        is_vip = True
        member_count = Member.list_members(is_count=True, is_vip=is_vip)
        members = [member_model.format_member(m) for m in Member.list_members(
            start=self.start, num=50, is_vip=is_vip, orderby="last_vip_at_desc")]
        self.render(
            "a_members/a_member_vips.html", num=50, members=members, member_id="",
            telephone="", member_count=member_count, is_staff=False
        )


class AdminMemberStaffHandler(JsSiteBaseHandler):
    @tornado.web.addslash
    @has_permission("member")
    def post(self, member_id):
        is_staff = self.get_argument("is_staff", "")
        if is_staff == "N":
            is_staff = False
        else:
            is_staff = True

        member = Member.load_member_by_member_id(member_id)
        if not member:
            self.data["message"] = "没有该用户"
            self.write(self.data)
            return

        Member.update_member({"telephone": member.telephone, "is_staff": is_staff})
        self.data["result"] = "success"
        self.write(self.data)


# /invites/
class AdminInvitesHandler(SiteBaseHandler):
    @tornado.web.addslash
    @has_permission("member")
    def get(self):
        invites = coupon_model.list_invite(self.start)
        self.render("a_coupons/a_invites.html", invites=invites)


urls = [
    (r"/members/?", AdminMembersHandler),
    (r"/members/vips/?", AdminMemberVipsHandler),
    (r"/member/detail/([a-z0-9-]+)/?", AdminMemberDetailHandler),
    (r"/member/staff/([a-z0-9-]+)/?", AdminMemberStaffHandler),
]


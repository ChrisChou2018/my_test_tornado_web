#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json

import bcrypt
import peewee
from peewee import fn, SQL

from app.models import base_model
import app.libs.common as lib_common




class Member(base_model.BaseModel):
    member_id = peewee.AutoField(db_column="member_id", primary_key=True)
    # login_name = peewee.CharField(db_column="LoginName")
    member_name = peewee.CharField(db_column="member_name")
    # password = peewee.CharField(db_column="LpassWord")
    hash_pwd = peewee.CharField(db_column="hash_pwd", default="")
    # member_lvl = peewee.CharField(db_column="MemberLvl")
    # member_score = peewee.CharField(db_column="MemberScore")
    telephone = peewee.CharField(db_column="telephone")
    # email = peewee.CharField(db_column="email")
    # pay_password = peewee.CharField(db_column="PayPassword")
    status = peewee.CharField(db_column="status")
    create_time = peewee.DateTimeField(db_column="create_time")
    salt_key = peewee.CharField(db_column="salt_key")
    # qq_openid = peewee.CharField(db_column="qq_openid")
    # update_time = peewee.DateTimeField(db_column="UpdateTime")
    # wb_openid = peewee.CharField(db_column="wb_openid")
    # sex = peewee.CharField(db_column="Sex")
    # birthday = peewee.CharField(db_column="Birthday")
    # member_num = peewee.CharField(db_column="MemberNum")
    # actual_member_lvl = peewee.CharField(db_column="ActualMemberLvl")
    # is_builtin = peewee.CharField(db_column="IsBuiltIn")
    role = peewee.CharField(db_column="role")
    sessions = peewee.CharField(db_column="sessions")
    # wx_openid = peewee.CharField(db_column="wx_openid")
    # created_ip = peewee.CharField(db_column="created_ip")
    # access_token = peewee.CharField(db_column="access_token")
    # member_avatar = peewee.CharField(db_column="member_avatar")
    # default_address_id = peewee.CharField(db_column="default_address_id")
    # skin_test_result = peewee.CharField(db_column="skin_test_result")
    # vip_avail_at = peewee.IntegerField(db_column='vip_avail_at')
    # vip_type = peewee.CharField()
    # last_vip_via = peewee.CharField()
    # last_vip_at = peewee.IntegerField()
    # is_staff = peewee.BooleanField(db_column="is_staff", default=False)
    # gold_coin = peewee.IntegerField(db_column="gold_coin", default=0)
    # account_balance = peewee.DecimalField(db_column="account_balance")
    # zero_buy_order_id = peewee.CharField(db_column="zero_buy_order_id", default="")
    # invite_vip_returns = peewee.DecimalField(default=0)
    # invite_vip_buys = peewee.DecimalField(default=0)

    class Meta:
        db_table = "app_member"

    def is_vip_valid(self):
        return self.vip_avail_at > time.time()
    
    @classmethod
    def create_member(cls, data):
        cls.create(**data)

    @classmethod
    def get_member_by_login(cls, member_name):
        try:
            return Member.get((Member.member_name == member_name) | \
                (Member.telephone == member_name))
        except Member.DoesNotExist:
            return None

    @classmethod
    def get_user_by_sess(self, telephone, session_id):
        member = None
        sessions = None

        try:
            member = Member.get(Member.telephone == telephone)
            sessions = json.loads(member.sessions)
        except:
            return None

        if not member or not sessions or not isinstance(sessions, list):
            return None

        for session in sessions:
            if isinstance(session, dict) and session.get("id") \
                    and session["id"] == session_id:
                return member

        return None

    @classmethod
    def find_telephone_by_memberid(cls, member_id):
        try:
            return Member.get(Member.member_id == member_id)
        except Member.DoesNotExist:
            return None


    @classmethod
    def get_member_by_telephone(cls, telephone):
        # status 为10表示邀请的用户，但是并未注册
        member_select = (Member.telephone == telephone)
        try:
            return Member.get(member_select)
        except Member.DoesNotExist:
            return None

    @classmethod
    def member_registration(cls, member_dict):
        member_dict["member_lvl"] = MemberGrading.get_uuid_by_default()
        return Member.create(**member_dict)

    @classmethod
    def update_member(cls, member_dict):
        return Member.update(**member_dict).where(
            Member.telephone == member_dict["telephone"]
        ).execute()

    @classmethod
    def update_pwd_by_telephone(cls, telephone, new_hash_pwd):
        # If member update their password, we use the bcrypt to encrypt.
        query = Member.update(password="", hash_pwd=new_hash_pwd)\
                      .where(Member.telephone == telephone)
        query.execute()

    @classmethod
    def find_old_psw_by_id(cls, member_id, password, encrypt="hash"):
        """the paramer `encrypt` has two way: md5 and hash
        """
        # Maybe the member still use old strage of password, so we
        # should still check if the member is still use old way to
        # store password
        if encrypt == "hash":
            try:
                return Member.get((Member.member_id == member_id) &
                                  (Member.hash_pwd == password))
            except Member.DoesNotExist:
                return None
        elif encrypt == "md5":
            try:
                return Member.get((Member.member_id == member_id) &
                                  (Member.password == password))
            except Member.DoesNotExist:
                return None

    @classmethod
    def update_pwd(cls, member_id, new_psw):
        # If member update their password, we use the bcrypt to encrypt.
        query = Member.update(hash_pwd=new_psw).where(Member.member_id == member_id)
        query.execute()

    # admin
    @classmethod
    def load_member_by_member_id(self, member_id):
        try:
            return Member.get(Member.member_id == member_id)
        except Member.DoesNotExist:
            return None

    @classmethod
    def get_member_by_name(cls, member_name):
        try:
            return Member.get(Member.member_name == member_name)
        except Member.DoesNotExist:
            return None
    
    @classmethod
    def get_member_by_id(cls, member_id):
        try:
            return Member.get(Member.member_id == member_id)
        except Member.DoesNotExist:
            return None

    # admin
    @classmethod
    def list_member_by_member_ids(cls, member_ids):
        if not member_ids:
            return []

        return [each for each in Member.select().where(
            Member.member_id.in_(member_ids))]

    # admin
    @classmethod
    def list_members(cls, member_id=None, telephone=None, is_staff=None, is_vip=False,
                     orderby=None, is_count=False, start=0, num=50, member_manager=False):
        member_select = (Member.status!="99")
        if member_id:
            member_id = "%"+member_id+"%"
            member_select = member_select&(Member.member_id ** member_id)
        if telephone:
            telephone = "%"+telephone+"%"
            member_select = member_select&(Member.telephone ** telephone)

        if is_staff is True:
            member_select = member_select&(Member.is_staff == "Y")
        elif is_staff is False:
            member_select = member_select&(Member.is_staff == "N")

        if is_vip:
            member_select = member_select&(Member.vip_avail_at > int(time.time()))

        if is_count:
            if member_manager:
                member_select = member_select&(Member.is_builtin=="1")
            return Member.select().where(member_select).count()

        if orderby == "last_vip_at_desc":
            order_cond = Member.last_vip_at.desc()
        else:
            order_cond = Member.create_time.desc()

        if member_manager:
            member_select = member_select&(Member.is_builtin=="1")
            return Member.select().where(member_select) \
                .order_by(Member.is_builtin.desc(), order_cond).offset(start).limit(num)
        else:
            return Member.select().where(member_select).order_by(order_cond) \
                .offset(start).limit(num)

    @classmethod
    def load_other_platform_member(cls, openid, platform="wechat"):
        if platform == "wechat":
            member_select = (Member.wx_openid==openid)
        elif platform == "qq":
            member_select = (Member.qq_openid==openid)
        elif platform == "sina":
            member_select = (Member.wb_openid==openid)

        try:
            return Member.get(member_select)
        except Member.DoesNotExist:
            return None

    @classmethod
    def update_member_by_member_ids(cls, member_ids, member_dict):
        Member.update(**member_dict).where(Member.member_id.in_(member_ids)).execute()

    @classmethod
    def list_members_by_builtin(cls):
        return [each for each in Member.select().where(
            (Member.status=="1")&(Member.is_builtin=="1")).order_by(fn.Rand())
        ]

    @classmethod
    def list_members_by_status(cls, status="1"):
        return [member for member in Member.select().where(
            Member.status==status
        )]

    @classmethod
    def list_member_id_by_create_time(cls, day="", is_count=False, begin_time="", end_time=""):
        member_select = (Member.status == "1")
        if day:
            member_select = member_select & (fn.timestampdiff(SQL("MINUTE"),
                Member.create_time, fn.now())>60*24*day)

        if begin_time and end_time:
            member_select = member_select & (Member.create_time.between(begin_time, end_time))

        if is_count:
            return Member.select().where(member_select).count()

        return [each.member_id for each in Member.select().where(member_select)]

    @classmethod
    def list_members_by_telephones(cls, telephones):
        return [member for member in Member.select().where(
            (Member.telephone.in_(telephones))&(Member.status!=99))
        ]

    @classmethod
    def get_member_obj(cls, current_page, search_value=None):
        if search_value:
            member_obj = Member.select().where(search_value).order_by(-Member.member_id).paginate(int(current_page), 15)
        else:
            member_obj = Member.select().order_by(-Member.member_id).paginate(int(current_page), 15)
        return member_obj
    
    @classmethod
    def get_member_obj_count(cls, search_value=None):
        if search_value:
            member_obj_count = Member.select().where(search_value).count()
        else:
            member_obj_count = Member.select().count()
        return member_obj_count

    @classmethod
    def update_member_by_member_id(cls, member_id, update_dict):
        Member.update(**update_dict).where(Member.member_id == member_id).execute()


def format_member(member):
    member.vip_avail_at_str = lib_common.timestamp2str(member.vip_avail_at) \
        if member.vip_avail_at > 0 else ""
    member.last_vip_at_str = lib_common.timestamp2str(member.last_vip_at) \
        if member.last_vip_at > 0 else ""

    member.vip_type_str = ""
    if member.vip_type == VIP_TYPE_HALF_YEAR:
        member.vip_type_str = "半年"
    elif member.vip_type == VIP_TYPE_ONE_YEAR:
        member.vip_type_str = "一年"

    return member


class MemberGrading(base_model.BaseModel):
    uuid = peewee.CharField(db_column="UUID", primary_key=True)
    order_num = peewee.CharField(db_column="OrderNum")
    name = peewee.CharField(db_column="Name")
    create_person = peewee.CharField(db_column="CreatePerson")
    create_time = peewee.DateTimeField(db_column="CreateTime")
    update_person = peewee.CharField(db_column="UpdatePerson")
    update_time = peewee.DateTimeField(db_column="Name")
    is_default = peewee.CharField(db_column="ISDefault")

    class Meta:
        db_table = "app_member_grading"

    @classmethod
    def get_uuid_by_default(cls):
        try:
            grading = MemberGrading.get(MemberGrading.is_default == "1")
            return grading.uuid
        except MemberGrading.DoesNotExist:
            return None


class IdentifyingCode(base_model.BaseModel):
    telephone = peewee.CharField(db_column="MemberId", primary_key=True)
    code = peewee.CharField(db_column="Code")
    create_time = peewee.DateTimeField(db_column="CreateTime")

    class Meta:
        db_table = "app_identifying_code"

    @classmethod
    def delete_code_by_telephone(cls, telephone):
        query = IdentifyingCode.delete().where(IdentifyingCode.telephone ==
            telephone)
        query.execute()

    @classmethod
    def insert_code_by_telephone(cls, telephone, code, create_time):
        return IdentifyingCode.create(telephone=telephone, code=code,
            create_time=create_time)

    @classmethod
    def find_validate_code(cls, code, telephone):
        try:
            return IdentifyingCode.get((IdentifyingCode.telephone==
                telephone)&(IdentifyingCode.code==code))
        except IdentifyingCode.DoesNotExist:
            return None


class Opinion(base_model.BaseModel):
    opinion_id = peewee.CharField(db_column="OpinionId", primary_key=True)
    title = peewee.CharField(db_column="Title")
    content = peewee.CharField(db_column="Content")
    create_person = peewee.CharField(db_column="CreatePerson")
    create_time = peewee.DateTimeField(db_column="CreateTime")
    status = peewee.CharField(db_column="Status")
    update_person = peewee.CharField(db_column="UpdatePerson")
    update_time = peewee.DateTimeField(db_column="UpdateTime")
    opinions_type = peewee.CharField(db_column="OpinionsType")
    contact = peewee.CharField(db_column="Contact")

    class Meta:
        db_table = "app_opinion"

    @classmethod
    def list_opinion(cls, start=0, num=50, is_count=False):
        opinion_select = (Opinion.status!="99")
        if is_count:
            return Opinion.select().where(opinion_select).count()

        return Opinion.select().where(opinion_select).order_by(
            Opinion.create_time.desc()).offset(start).limit(num)

    @classmethod
    def update_opinion(cls, opinion_id, opinion_dict):
        Opinion.update(**opinion_dict).where(Opinion.opinion_id==opinion_id).execute()


class Address(base_model.BaseModel):
    address_id = peewee.CharField(db_column="AddressId", primary_key=True)
    member_id = peewee.CharField(db_column="MemberId")
    addressee = peewee.CharField(db_column="Addressee")
    address = peewee.CharField(db_column="Address")
    telephone = peewee.CharField(db_column="Telephone")
    zip_code = peewee.CharField(db_column="ZipCode")
    create_time = peewee.DateTimeField(db_column="CreateTime")
    update_time = peewee.DateTimeField(db_column="UpdateTime")
    area = peewee.CharField(db_column="Area")
    status = peewee.CharField(db_column="status", default="normal")

    class Meta:
        db_table = "app_address"

    @classmethod
    def find_all(cls, member_id):
        return Address.select().where((Address.member_id==member_id)&(
            Address.status!="deleted")).order_by(Address.create_time.desc()
        )

    @classmethod
    def find_by_id(cls, address_id):
        try:
            return Address.get((Address.address_id==address_id)&(Address.status!="deleted"))
        except Address.DoesNotExist:
            return None

    @classmethod
    def load_address_by_id(cls, address_id):
        try:
            return Address.get((Address.address_id==address_id)&(Address.status!="deleted"))
        except Address.DoesNotExist:
            return None

    @classmethod
    def load_address_by_cond(cls, address_dict):
        try:
            return Address.get(
                (Address.member_id==address_dict["member_id"])&
                (Address.addressee==address_dict["addressee"])&
                (Address.telephone==address_dict["telephone"])&
                (Address.address==address_dict["address"])
            )
        except Address.DoesNotExist:
            return None

    @classmethod
    def delete_by_id(cls, address_id):
        Address.update(status="deleted").where(Address.address_id==address_id).execute()

    @classmethod
    def list_address_by_member_id(cls, member_id):
        return Address.select().where((Address.member_id==member_id)&(
            Address.status!="deleted")).order_by(Address.create_time.desc()
        )


class CheckinLog(base_model.BaseModel):
    """签到
    """
    id = peewee.CharField(db_column="ID", primary_key=True)
    member_id = peewee.CharField(db_column="MemberId")
    create_time = peewee.DateTimeField(db_column="CreateTime")
    update_time = peewee.DateTimeField(db_column="UpdateTime")
    checkin_count = peewee.IntegerField(db_column="CheckinCount")

    class Meta:
        db_table = "app_checkin_logs"

    @classmethod
    def list_checkin_logs(cls, member_id):
        return CheckinLog.select()\
                         .where(CheckinLog.member_id == member_id)\
                         .order_by(CheckinLog.create_time.desc())

    @classmethod
    def load_nearest_checkin(cls, member_id):
        """get the nearest check in log"""
        try:
            return CheckinLog.select()\
                             .where(CheckinLog.member_id == member_id)\
                             .order_by(CheckinLog.create_time.desc())\
                             .get()
        except CheckinLog.DoesNotExist:
            return None

    @classmethod
    def insert_log(cls, log):
        CheckinLog.create(**log)


class MemberCoinLog(base_model.BaseModel):
    """金币变化

    change_type: 变化类型, checkin(签到)、exchange(兑换)
    """
    id = peewee.CharField(db_column="ID", primary_key=True)
    member_id = peewee.CharField(db_column="MemberId")
    create_time = peewee.DateTimeField(db_column="CreateTime")
    update_time = peewee.DateTimeField(db_column="UpdateTime")
    coin_change = peewee.IntegerField(db_column="CoinChange")
    change_type = peewee.CharField(db_column="ChangeType")
    coupon_id = peewee.CharField(db_column="CouponID", default="")

    class Meta:
        db_table = "app_coin_logs"

    @classmethod
    def list_coin_log(cls, member_id, change_type=None):
        """根据变化类型，获取相关记录"""
        select_query = (MemberCoinLog.member_id == member_id)
        if change_type:
            select_query = (select_query) & (MemberCoinLog.change_type == change_type)

        return MemberCoinLog.select()\
                             .where(select_query)\
                            .order_by(MemberCoinLog.create_time.desc())

    @classmethod
    def insert_log(cls, log):
        MemberCoinLog.create(**log)


class MemberAccLog(base_model.BaseModel):
    log_id = peewee.IntegerField(db_column="id", primary_key=True)
    member_id = peewee.CharField(db_column="member_id")
    amount = peewee.DecimalField(db_column="amount")
    reason = peewee.CharField(db_column="reason")
    reason_desc = peewee.CharField(db_column="reason_desc")
    created_at = peewee.IntegerField(db_column="created_at")

    class Meta:
        db_table = "app_member_acc_logs"


def change_account_balance(member_id, amount, reason, reason_desc=""):
    if not reason in ACC_CHG_REASON_DESCS:
        return False
    member = Member.load_member_by_member_id(member_id)
    if not member:
        return False

    member.account_balance = (int(member.account_balance * 100) + int(amount * 100)) / 100.0
    if member.account_balance < 0:
        return False
    member.save()

    acc_log = MemberAccLog(member_id=member_id, amount=amount, reason=reason,
        reason_desc=ACC_CHG_REASON_DESCS[reason], created_at=int(time.time()))
    acc_log.save()

    return True


def list_account_balance_logs(member_id):
    sel_query = (MemberAccLog.member_id == member_id)
    log_cursor = MemberAccLog.select().where(sel_query).order_by(MemberAccLog.created_at.desc())
    logs = [build_acc_balance_log_dict(log) for log in log_cursor]
    return logs

def build_acc_balance_log_dict(log):
    log_dict = {
        "id": log.log_id, "amount": str(log.amount), "reason": log.reason,
        "reason_desc": log.reason_desc, "created_at": log.created_at,
        "created_at_str": lib_common.timestamp2str(log.created_at)
    }
    return log_dict


def re_calc_invite_returns(member_id):
    # 返利
    invite_vip_returns = MemberAccLog.select(fn.SUM(MemberAccLog.amount)).where(
        (MemberAccLog.member_id == member_id) & (MemberAccLog.reason == ACC_CHG_REASON_INVITE_VIP)
    ).scalar()
    # 返现
    invite_vip_buys = MemberAccLog.select(fn.SUM(MemberAccLog.amount)).where(
        (MemberAccLog.member_id == member_id) & (MemberAccLog.reason == ACC_CHG_REASON_INVITE_BUY)
    ).scalar()

    update_member_by_member_id(
        member_id, {"invite_vip_returns": invite_vip_returns, "invite_vip_buys": invite_vip_buys}
    )


ACC_CHG_REASON_INVITE_VIP = "invite_vip"
ACC_CHG_REASON_INVITE_BUY = "invite_buy"
ACC_CHG_REASON_ORDER_SPENDING = "order_spending"
ACC_CHG_REASON_DESCS = {
    ACC_CHG_REASON_INVITE_VIP: "VIP 邀请返利",
    ACC_CHG_REASON_INVITE_BUY: "邀请购买返现",
    ACC_CHG_REASON_ORDER_SPENDING: "订单消费",
}

VIP_TYPE_ONE_YEAR = "one_year"
VIP_TYPE_HALF_YEAR = "half_year"
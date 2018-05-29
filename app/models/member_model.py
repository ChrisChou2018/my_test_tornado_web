#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json

import bcrypt
import peewee

from app.models import base_model
import app.libs.common as lib_common


class Member(base_model.BaseModel):
    member_id           = peewee.AutoField(db_column="member_id", primary_key=True)
    member_name         = peewee.CharField(db_column="member_name")
    hash_pwd            = peewee.CharField(db_column="hash_pwd")
    telephone           = peewee.CharField(db_column="telephone")
    status              = peewee.CharField(db_column="status")
    salt_key            = peewee.CharField(db_column="salt_key")
    role                = peewee.CharField(db_column="role", null=True)
    sessions            = peewee.CharField(db_column="sessions")
    created_ip          = peewee.CharField(db_column="created_ip", null=True)
    is_builtin          = peewee.CharField(db_column="is_builtin")
    create_time         = peewee.IntegerField(db_column="create_time")
    update_time         = peewee.IntegerField(db_column="update_time")
    

    class Meta:
        db_table = "app_member"
    
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
    def get_user_by_sess(cls, member_id, session_id):
        member = None
        sessions = None
        try:
            member = cls.get(cls.member_id == member_id)
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
    def get_member_by_telephone(cls, telephone):
        # status 为10表示邀请的用户，但是并未注册
        member_select = (Member.telephone == telephone)
        try:
            return Member.get(member_select)
        except Member.DoesNotExist:
            return None

    @classmethod
    def update_pwd_by_telephone(cls, telephone, new_hash_pwd):
        # If member update their password, we use the bcrypt to encrypt.
        query = Member.update(password="", hash_pwd=new_hash_pwd)\
                      .where(Member.telephone == telephone)
        query.execute()

    @classmethod
    def update_pwd(cls, member_id, new_psw):
        # If member update their password, we use the bcrypt to encrypt.
        query = Member.update(hash_pwd=new_psw).where(Member.member_id == member_id)
        query.execute()

    @classmethod
    def get_member_by_member_name(cls, member_name):
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

    @classmethod
    def update_member_by_member_ids(cls, member_ids, member_dict):
        Member.update(**member_dict).where(Member.member_id.in_(member_ids)).execute()

    @classmethod
    def list_members_by_status(cls, status="1"):
        return [member for member in Member.select().where(
            Member.status==status
        )]


    @classmethod
    def get_member_list(cls, current_page, search_value=None):
        if search_value:
            member_obj = Member.select().where(search_value).order_by(-Member.member_id).paginate(int(current_page), 15)
        else:
            member_obj = Member.select().order_by(-Member.member_id).paginate(int(current_page), 15)
        return member_obj
    
    @classmethod
    def get_member_count(cls, search_value=None):
        if search_value:
            member_obj_count = Member.select().where(search_value).count()
        else:
            member_obj_count = Member.select().count()
        return member_obj_count

    @classmethod
    def update_member_by_member_id(cls, member_id, update_dict):
        Member.update(**update_dict).where(Member.member_id == member_id).execute()


# class IdentifyingCode(base_model.BaseModel):
#     telephone           = peewee.CharField(db_column="MemberId", primary_key=True)
#     code                = peewee.CharField(db_column="Code")
#     create_time         = peewee.DateTimeField(db_column="CreateTime")

#     class Meta:
#         db_table = "app_identifying_code"

#     @classmethod
#     def delete_code_by_telephone(cls, telephone):
#         query = IdentifyingCode.delete().where(IdentifyingCode.telephone ==
#             telephone)
#         query.execute()

#     @classmethod
#     def insert_code_by_telephone(cls, telephone, code, create_time):
#         return IdentifyingCode.create(telephone=telephone, code=code,
#             create_time=create_time)

#     @classmethod
#     def find_validate_code(cls, code, telephone):
#         try:
#             return IdentifyingCode.get((IdentifyingCode.telephone==
#                 telephone)&(IdentifyingCode.code==code))
#         except IdentifyingCode.DoesNotExist:
#             return None



# class MemberGrading(base_model.BaseModel):
#     uuid = peewee.CharField(db_column="UUID", primary_key=True)
#     order_num = peewee.CharField(db_column="OrderNum")
#     name = peewee.CharField(db_column="Name")
#     create_person = peewee.CharField(db_column="CreatePerson")
#     create_time = peewee.DateTimeField(db_column="CreateTime")
#     update_person = peewee.CharField(db_column="UpdatePerson")
#     update_time = peewee.DateTimeField(db_column="Name")
#     is_default = peewee.CharField(db_column="ISDefault")

#     class Meta:
#         db_table = "app_member_grading"

#     @classmethod
#     def get_uuid_by_default(cls):
#         try:
#             grading = cls.get(cls.is_default == "1")
#             return grading.uuid
#         except cls.DoesNotExist:
#             return None


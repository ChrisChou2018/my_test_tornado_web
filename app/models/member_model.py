#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json

import bcrypt
import peewee

from app.models import base_model
import app.libs.common as lib_common


class Member(base_model.BaseModel):
    member_id = peewee.AutoField(db_column="member_id", primary_key=True)
    member_name = peewee.CharField(db_column="member_name")
    hash_pwd = peewee.CharField(db_column="hash_pwd")
    telephone = peewee.CharField(db_column="telephone")
    status = peewee.CharField(db_column="status")
    create_time = peewee.DateTimeField(db_column="create_time")
    salt_key = peewee.CharField(db_column="salt_key")
    role = peewee.CharField(db_column="role")
    sessions = peewee.CharField(db_column="sessions")
    

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



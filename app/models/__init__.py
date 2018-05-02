#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import member_model
if not member_model.Member.table_exists:
    member_model.Member.create_table(safe=True)


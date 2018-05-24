#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import member_model
from app.models import items_model

def init_table():
    if not member_model.Member.table_exists():
        member_model.Member.create_table(safe=True)
    if not items_model.Items.table_exists():
        items_model.Items.create_table(safe=True)
    if not items_model.ItemImages.table_exists():
        items_model.ItemImages.create_table(safe=True)
    print('finish....')
    
# init_table()


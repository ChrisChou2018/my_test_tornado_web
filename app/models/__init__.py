#!/usr/bin/env python
# -*- coding: utf-8 -*-
import peewee

from app.models import member_model
from app.models import items_model


models_file_list = [
    member_model,
    items_model
]

def init_table():
    for models in models_file_list:
        for model in dir(models):
            model_obj = getattr(models, model)
            if isinstance(model_obj, peewee.ModelBase) and \
                not model_obj.table_exists():
                model_obj.create_table(safe=True)
    else:
        print('finish....')



#!/usr/bin/env python
# -*- coding: utf-8 -*-

from meihuishuo.handlers.admin.a_members import *
from meihuishuo.handlers.admin.a_activities import *


ADMIN_EXT_URLS = [
    (r"/invites/?", AdminInvitesHandler),
    (r"/activities/zero-buy-goods/?", AdminActivityZeroBuyGoodsHandler),
]
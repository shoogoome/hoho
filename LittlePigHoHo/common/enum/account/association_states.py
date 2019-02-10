# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class AccountStatesEnum(EnumBase):

    PENDING = 0
    SUCCESS = 1
    FAIL = 2

    __default__ = PENDING

    __desc__ = {
        'PENDING': '待审核',
        'SUCCESS': '审核通过',
        'FAIL': '申请驳回',
    }
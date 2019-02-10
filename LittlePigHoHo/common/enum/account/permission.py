# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class AccountPermissionEnum(EnumBase):

    VIEWS = 1
    CREATE_ASSOCIATION = 2

    __default__ = VIEWS

    __desc__ = {
        'VIEWS': '查看',
        'CREATE_ASSOCIATION': '创建协会权限'
    }
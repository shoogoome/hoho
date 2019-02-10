# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase


class PermiumLevelEnum(EnumBase):

    # 普通用户
    FREE = 0
    # 高级用户
    DELUXE = 1

    __default__ = FREE
    __desc__ = {
        "FREE": "普通用户",
        "DELUXE": "高级用户",
    }
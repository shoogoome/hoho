# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class SexEnum(EnumBase):

    UNKNOW = 0
    MALE = 1
    FEMALE = 2

    __default__ = UNKNOW
    __desc__ = {
        'UNKNOW': '未知',
        'MALE': '男生',
        'FEMALE': '女生',
    }

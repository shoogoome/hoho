# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase


class RoleEnum(EnumBase):

    DIRECTOR = 0
    MINISTER = 1
    PRESIDENT = 2
    TEACHER = 4
    ADMIN = 99

    __default__ = DIRECTOR
    __desc__ = {
        'DIRECTOR': '干事',
        'MINISTER': '部长',
        'PRESIDENT': '会长',
        'TEACHER': '老师',
        'ADMIN': '系统管理员',
    }
# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class AssociationPermissionEnum(EnumBase):

    ASSOCIATION = 0
    ATTENDANCE = 1
    APPRAISING = 2
    INTERVIEW = 4
    NOTICE = 8
    REPOSITORY = 16
    SCHEDULING = 32
    TASK = 64
    DEPARTMENT = 128

    ASSOCIATION_VIEW_DATA = 256
    ATTENDANCE_SIGN = 512

    __default__ = ASSOCIATION

    __desc__ = {
        'ASSOCIATION': '协会',
        'ASSOCIATION_VIEW_DATA': '协会敏感数据查看',
        'ATTENDANCE': '考勤',
        'ATTENDANCE_SIGN': '签到',
        'DEPARTMENT': '部门',
        'APPRAISING': '绩效考核',
        'INTERVIEW': '面试',
        'NOTICE': '通知',
        'REPOSITORY': '资源',
        'SCHEDULING': '排班',
        'TASK': '任务',
    }
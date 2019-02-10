# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class AssociationPermissionEnum(EnumBase):

    VIEWS = 1
    MANAGE = 2
    ADDDIRECTOR = 4

    ATTENDANCE = 8
    ATTENDANCE_VIEW = 16
    ATTENDANCE_CREATE = 32
    ATTENDANCE_MANAGE = 64

    DEPARTMENT_CREATE = 1028
    DEPARTMENT_VIEW = 2056
    DEPARTMENT_DELETE = 4112
    DEPARTMENT_MANAGE = 8224

    __default__ = VIEWS

    __desc__ = {
        'VIEWS': '查看',
        'MANAGE': '管理',
        'ATTENDANCE': '签到',
        'ADDDIRECTOR': '添加干事权限',
        'ATTENDANCE_VIEW': '考勤查看情况',
        'ATTENDANCE_CREATE': '创建考勤',
        'ATTENDANCE_MANAGE': '管理考勤',
        'DEPARTMENT_CREATE': '创建部门',
        'DEPARTMENT_VIEW': '查看部门',
        'DEPARTMENT_DELETE': '删除部门',
        'DEPARTMENT_MANAGE': '管理部门',
    }
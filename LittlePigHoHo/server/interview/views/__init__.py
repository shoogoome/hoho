# -*- coding:utf-8 -*-
# coding:utf-8
from .registration import RegistrationInfo, RegistrationView
from .info import RegistrationTemplateInfo, RegistrationTemplateView
from .manage import InterviewManage

__all__ = [
    # 报名表
    'RegistrationInfo', 'RegistrationView',
    # 报名表模板
    'RegistrationTemplateInfo', 'RegistrationTemplateView',
    # 管理
    'InterviewManage'
]

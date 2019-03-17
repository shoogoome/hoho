 # -*- coding: utf-8 -*-
# coding:utf-8

from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager


# 学校表
class School(models.Model):

    class Meta:
        verbose_name = "学校"
        verbose_name_plural = "学校表"
        app_label='school'

    # 学校名称
    name = models.CharField(max_length=50)

    # 学校缩写（小写）
    short_name = models.CharField(max_length=10, default="", blank=True)

    # 学校标志（图像文件）
    logo = models.CharField(max_length=255, default="", blank=True)

    # 学校简介
    description = models.CharField(max_length=255, default="",  blank=True)

    # 学校配置信息(用户可以改动的部分)
    config = models.TextField(default='{}')

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[%s] %s(%s)" % (self.id, self.name, self.short_name)

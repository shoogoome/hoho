 # -*- coding: utf-8 -*-
# coding:utf-8

from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager
from common.core.dao.cache.factory import delete_model_single_object_cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from common.core.dao.time_stamp import TimeStampField


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

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[%s] %s(%s)" % (self.id, self.name, self.short_name)

receiver(post_save, sender=School)(delete_model_single_object_cache)
receiver(post_delete, sender=School)(delete_model_single_object_cache)

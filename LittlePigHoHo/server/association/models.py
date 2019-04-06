# -*- coding: utf-8 -*-
# coding:utf-8

from django.db import models

from common.enum.account.permiumLevel import PermiumLevelEnum
from common.enum.account.role import RoleEnum
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete
from common.core.dao.cache.model_manager import HoHoModelManager
from common.core.dao.cache.factory import bind_model_cached_manager_signal
from common.core.dao.cache.factory import delete_model_single_object_cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from common.entity.association.permissions import AssociationPermissionsEntity
from common.entity.association.backlog import AssociationBacklog
from common.entity.association.config import AssociationConfigureEntity

from common.core.dao.time_stamp import TimeStampField


# 协会表
class Association(models.Model):
    class Meta:
        verbose_name = "协会"
        verbose_name_plural = "协会表"
        app_label = 'association'

    # 归属学校
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)

    # 协会名称
    name = models.CharField(max_length=50)

    # 协会缩写（小写）
    short_name = models.CharField(max_length=10, default="", db_index=True)

    # 协会标志（图像文件）
    logo = models.CharField(max_length=255, default="", blank=True)

    # 协会简介
    description = models.CharField(max_length=255, default="", blank=True)

    # 代办事项
    backlog = models.TextField(default=AssociationBacklog().dumps())

    # 协会配置信息(评优配置数据)
    config = models.TextField(default=AssociationConfigureEntity().dumps())

    # 是否集群（有无部门）模式
    colony = models.BooleanField(default=False)

    # 协会仓库最大空间（默认2G)
    repository_size = models.BigIntegerField(default=2147483648)

    # 协会码
    choosing_code = models.CharField(default='', max_length=15, blank=True)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[%s] %s(%s)" % (self.id, self.name, self.short_name)


class AssociationDepartment(models.Model):
    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门表"
        app_label = 'association'

    # 部门名称
    name = models.CharField(max_length=64, default="")

    # 部门缩写（小写）
    short_name = models.CharField(max_length=10, default="", db_index=True)

    # 部门简介
    description = models.CharField(max_length=255, default="", blank=True)

    # 部门配置信息(用户可以改动的部分)
    config = models.TextField(default='{}')

    # 归属协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 部长
    manager = models.ManyToManyField('association.AssociationAccount', blank=True,
                                                  related_name='department_manager')

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}]{}:{}".format(self.id, self.name, self.association.name)


class AssociationAccount(models.Model):
    class Meta:
        verbose_name = "协会人事"
        verbose_name_plural = "协会人事表"
        app_label = 'association'

    # 协会内名称
    nickname = models.CharField(max_length=50, default="")

    # 关联用户
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 关联部门
    department = models.ForeignKey('association.AssociationDepartment', on_delete=models.CASCADE, null=True, blank=True)

    # 用户角色
    role = models.PositiveSmallIntegerField(**RoleEnum.get_models_params())

    # 权限
    permissions = models.TextField(default=AssociationPermissionsEntity().dumps())

    # 退休换届与否
    retire = models.BooleanField(default=False)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[%d] %s %s" % (self.id, self.role, self.nickname)


class AssociationAttendance(models.Model):
    class Meta:
        verbose_name = "协会考勤"
        verbose_name_plural = "协会考勤表"
        app_label = 'association'

    # 考勤名称
    title = models.CharField(max_length=64, default="")

    # 考勤发起者
    author = models.ForeignKey('association.AssociationAccount', null=True, on_delete=models.SET_NULL)

    # 归属协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 描述
    description = models.TextField(default="", blank=True)

    # 考勤地点(纬度)
    place_x = models.FloatField(default=0.0)

    # 考勤地点(经度)
    place_y = models.FloatField(default=0.0)

    # 容错距离(半径m)
    distance = models.FloatField(default=50.0)

    # 开始时间
    start_time = models.FloatField(default=0.0)

    # 结束时间
    end_time = models.FloatField(default=0.0)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[%s] 标题:%s, 归属协会%s" % (self.id, self.title, self.association.name)


receiver(post_save, sender=AssociationAttendance)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationAttendance)(delete_model_single_object_cache)

receiver(post_save, sender=Association)(delete_model_single_object_cache)
receiver(post_delete, sender=Association)(delete_model_single_object_cache)

receiver(post_save, sender=AssociationDepartment)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationDepartment)(delete_model_single_object_cache)

receiver(post_save, sender=AssociationAccount)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationAccount)(delete_model_single_object_cache)



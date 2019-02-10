# -*- coding: utf-8 -*-
# coding:utf-8

from django.db import models

from common.enum.account.permiumLevel import PermiumLevelEnum
from common.enum.account.role import RoleEnum
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete

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

    # 待办事项
    backlog = models.TextField(default='{}')

    # 协会配置信息(用户可以改动的部分)
    config = models.TextField(default='{}')

    # 付费等级
    premium_level = models.PositiveSmallIntegerField(**PermiumLevelEnum.get_models_params())

    # 付费到期时间
    premium_deadline = models.FloatField(default=0)

    # 协会仓库最大空间（默认2G)
    repository_size = models.BigIntegerField(default=2147483648)

    # 协会码
    choosing_code = models.CharField(default='', max_length=15, blank=True)

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
    master_administrator = models.ManyToManyField('account.Account', blank=True,
                                                  related_name='department_administrator')


class AssociationAccount(models.Model):
    class Meta:
        verbose_name = "协会人事"
        verbose_name_plural = "协会人事表"
        app_label = 'association'

    # 关联用户
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 关联部门
    department = models.ForeignKey('association.AssociationDepartment', on_delete=models.CASCADE, null=True, blank=True)

    # 用户角色
    role = models.PositiveSmallIntegerField(**RoleEnum.get_models_params())

    def __str__(self):
        return "[%d] %s-%s %s" % (self.id, self.association.name, self.department.name, self.account.realname)


class AssociationAttendance(models.Model):
    class Meta:
        verbose_name = "协会考勤情况"
        verbose_name_plural = "协会考勤情况表"
        app_label = 'association'

    # 考勤名称
    title = models.CharField(max_length=64, default="")

    # 版本号
    version = models.FloatField(default=0.0)

    # 考勤发起者
    author = models.ForeignKey('account.Account', null=True, on_delete=models.SET_NULL)

    # 归属协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 描述
    description = models.TextField(default="", blank=True)

    # 考勤地点
    place = models.CharField(max_length=64, default="", blank=True)

    # 开始时间
    start_time = models.FloatField(default=0.0)

    # 结束时间
    end_time = models.FloatField(default=0.0)

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[%s] 标题:%s, 归属协会%s" % (self.id, self.title, self.association.name)



@receiver(post_save, sender=AssociationAttendance)
def version_selfadd(instance, **kwargs):
    """
    自增版本号
    :param instance:
    :param kwargs:
    :return:
    """
    if kwargs.get('create', False) is True:
        instance.version = AssociationAttendance.objects.all().order_by('version')[-1] + 1
        instance.save()



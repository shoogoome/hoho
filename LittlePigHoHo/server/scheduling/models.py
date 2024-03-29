from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .logic.redis import SchedulingRedis
from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import HoHoModelManager
from common.core.dao.time_stamp import TimeStampField


class AssociationCurriculum(models.Model):
    """
    无课表
    """

    class Meta:
        verbose_name = "无课表"
        verbose_name_plural = "无课表"
        app_label = 'scheduling'

    # 标题
    title = models.CharField(max_length=100)

    # 协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 内容
    content = models.TextField(default='{}')

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "%d %s" % (self.id, self.title)

class AssociationAccountCurriculum(models.Model):
    """
    用户无课表
    """

    class Meta:
        verbose_name = "用户无课表"
        verbose_name_plural = "用户无课表"
        app_label = 'scheduling'

    # 用户
    account = models.ForeignKey('association.AssociationAccount', on_delete=models.CASCADE)

    # 无课表
    curriculum = models.ForeignKey('scheduling.AssociationCurriculum', on_delete=models.CASCADE)

    # 内容
    content = models.TextField(default='{}')

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "{} {} {}".format(
            self.id,
            self.account.account.realname,
            self.curriculum.title
        )

class AssociationScheduling(models.Model):
    """
    排班表
    """

    class Meta:
        verbose_name = "协会排班"
        verbose_name_plural = "协会排班表"
        app_label = 'scheduling'

    # 发起人
    author = models.ForeignKey('association.AssociationAccount', on_delete=models.SET_NULL, null=True, blank=True)

    # 协会关联
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 标题
    title = models.CharField(max_length=255)

    # 配置
    config = models.TextField(default="{}")

    # 排班表
    content = models.TextField(default="{}")

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
        return "[{}] {} {}".format(self.id, self.title, self.association.name)



def update_cache(instance, **kwargs):
    # 清除数据库缓存
    delete_model_single_object_cache(instance, **kwargs)
    # 课表变动则删除缓存
    redis = SchedulingRedis()
    name = str(instance.curriculum.association_id)
    redis.delete(name)


receiver(post_save, sender=AssociationAccountCurriculum)(update_cache)
receiver(post_delete, sender=AssociationAccountCurriculum)(update_cache)

receiver(post_save, sender=AssociationCurriculum)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationCurriculum)(delete_model_single_object_cache)

receiver(post_save, sender=AssociationScheduling)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationScheduling)(delete_model_single_object_cache)


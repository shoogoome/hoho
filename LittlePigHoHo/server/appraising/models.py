from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager
from common.core.dao.cache.factory import delete_model_single_object_cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from common.core.dao.time_stamp import TimeStampField
import json
from common.core.dao.redis import get_redis_conn
from .logic.redis import AppraisingRedis

class AppraisingScoreTemplate(models.Model):

    class Meta:
        verbose_name = "评分模板"
        verbose_name_plural = "评分模板表"
        app_label = 'appraising'

    # 发起人
    author = models.ForeignKey('association.AssociationAccount', blank=True, on_delete=models.SET_NULL, null=True)

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 标题
    title = models.CharField(max_length=255)

    # 配置 目前只支持单选题目形式
    config = models.TextField(default="[]")

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.title, self.association.name)


class AppraisingScore(models.Model):

    class Meta:
        verbose_name = "评分"
        verbose_name_plural = "评分表"
        app_label = 'appraising'

    # 填写人
    author = models.ForeignKey('association.AssociationAccount',
                               blank=True, on_delete=models.SET_NULL, null=True, related_name='appraising_score_author')

    # 版本号
    version = models.IntegerField(default=0)

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 面向对象
    target = models.ForeignKey('association.AssociationAccount', on_delete=models.CASCADE, related_name='appraising_score_target')

    # 使用模版
    template = models.ForeignKey('appraising.AppraisingScoreTemplate', on_delete=models.CASCADE)

    # 正文
    content = models.TextField(default="{}")

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 总分
    score = models.FloatField(default=0.0)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {}->{} {}".format(self.id, self.author.nickname, self.target.nickname, self.association.name)


def update_cache(instance, **kwargs):
    # 清除数据库缓存
    delete_model_single_object_cache(instance, **kwargs)
    # 评价变动则删除缓存
    redis = AppraisingRedis()
    name = "{}:{}".format(instance.association_id, instance.version)
    if redis.exists(name):
        redis.delete(name)


receiver(post_save, sender=AppraisingScore)(update_cache)
receiver(post_delete, sender=AppraisingScore)(update_cache)

receiver(post_save, sender=AppraisingScoreTemplate)(delete_model_single_object_cache)
receiver(post_delete, sender=AppraisingScoreTemplate)(delete_model_single_object_cache)













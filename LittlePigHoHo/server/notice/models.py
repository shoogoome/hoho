from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager
from common.core.dao.cache.factory import bind_model_cached_manager_signal
from common.core.dao.cache.factory import delete_model_single_object_cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from common.core.dao.time_stamp import TimeStampField


# Create your models here.


class AssociationNotice(models.Model):
    class Meta:
        verbose_name = "通知"
        verbose_name_plural = "通知表"
        app_label = 'notice'

    # 发起人
    author = models.ForeignKey('association.AssociationAccount', on_delete=models.CASCADE)

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 关联部门
    department = models.ForeignKey('association.AssociationDepartment', on_delete=models.CASCADE, blank=True, null=True)

    # 标题
    title = models.CharField(max_length=255)

    # 通知正文
    content = models.TextField(default="")

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

receiver(post_save, sender=AssociationNotice)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationNotice)(delete_model_single_object_cache)


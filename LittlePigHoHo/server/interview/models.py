from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete
from common.core.dao.cache.model_manager import HoHoModelManager
from common.core.dao.cache.factory import bind_model_cached_manager_signal
from common.core.dao.cache.factory import delete_model_single_object_cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from common.core.dao.time_stamp import TimeStampField


# Create your models here.

class InterviewRegistrationTemplate(models.Model):
    class Meta:
        verbose_name = "报名表模版"
        verbose_name_plural = "报名表模版表"
        app_label = 'interview'

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 创建人
    author = models.ForeignKey('association.AssociationAccount', blank=True, on_delete=models.SET_NULL, null=True)

    # 标题
    title = models.CharField(max_length=255)

    # 配置
    config = models.TextField(default='{}')

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()


    def __str__(self):
        return "[{}]{} {}".format(self.id, self.association.name, self.title)


class InterviewRegistration(models.Model):
    class Meta:
        verbose_name = "报名表"
        verbose_name_plural = "报名表"
        app_label = 'interview'

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 版本号
    version = models.IntegerField(default=0)

    # 关联账户
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 正文信息
    content = models.TextField(default='{}')

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.association.name, self.account.realname)



receiver(post_save, sender=InterviewRegistration)(delete_model_single_object_cache)
receiver(post_delete, sender=InterviewRegistration)(delete_model_single_object_cache)

receiver(post_save, sender=InterviewRegistrationTemplate)(delete_model_single_object_cache)
receiver(post_delete, sender=InterviewRegistrationTemplate)(delete_model_single_object_cache)



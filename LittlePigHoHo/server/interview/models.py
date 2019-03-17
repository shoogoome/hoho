from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete
from common.core.dao.cache.model_manager import HoHoModelManager

# Create your models here.


class InterviewRegistrationTemplate(models.Model):
    class Meta:
        verbose_name = "报名表模版"
        verbose_name_plural = "报名表模版表"
        app_label = 'interview'

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 标题
    title = models.CharField(max_length=255)

    # 附加信息
    additional = models.TextField(default='{}')

    # 启用与否
    using = models.BooleanField(default=False)

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True)

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

    # 关联账户
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 附加信息
    additional = models.TextField(default='{}')

    # 是否淘汰
    eliminate = models.BooleanField(default=False)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.association.name, self.account.realname)


from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager

# Create your models here.

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

    # 配置
    config = models.TextField(default="{}")

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True)

    # 管理员
    manager = models.ManyToManyField('association.AssociationAccount', blank=True, related_name='notice_manager')

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
    author = models.ForeignKey('association.AssociationAccount', blank=True, on_delete=models.SET_NULL, null=True)

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 使用模版
    template = models.ForeignKey('appraising.AppraisingScoreTemplate', on_delete=models.CASCADE)

    # 正文
    content = models.TextField(default="{}")

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.author.nickname, self.association.name)

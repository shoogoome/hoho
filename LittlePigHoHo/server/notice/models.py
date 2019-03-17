from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager

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
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True)

    # 管理员
    manager = models.ManyToManyField('association.AssociationAccount', blank=True, related_name='notice_manager')

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.title, self.association.name)
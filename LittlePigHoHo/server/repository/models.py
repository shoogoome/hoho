from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager


class RepositoryFile(models.Model):

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = "文件表"

    # 上传者
    author = models.ForeignKey('association.AssociationAccount', on_delete=models.SET_NULL, null=True, blank=True)

    # 归属协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 文件名
    title = models.CharField(max_length=255)

    # 描述
    description = models.TextField(default="")

    # 文件地址
    path = models.CharField(max_length=200, default='', blank=True)

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {} {}".format(self.id, self.association.name, self.title, self.author.nickname)
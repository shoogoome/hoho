from django.db import models

class Curriculum(models.Model):
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

    # 描述
    description = models.CharField(max_length=255, default="",  blank=True)

    # 内容
    content = models.TextField(default='{}')

    def __str__(self):
        return "%d %s" % (self.id, self.title)

class AccountCurriculum(models.Model):
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
    curriculum = models.ForeignKey('scheduling.Curriculum', on_delete=models.CASCADE)

    # 内容
    content = models.TextField(default='{}')

    def __str__(self):
        return "%d %s %s".format(
            self.id,
            self.account.account.realname,
            self.curriculum.title
        )

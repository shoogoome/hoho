from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager

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
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)

    # 描述
    description = models.CharField(max_length=255, default="",  blank=True)

    # 内容
    content = models.TextField(default='{}')

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

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "%d %s %s".format(
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
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True)

    # 管理员
    manager = models.ManyToManyField('association.AssociationAccount', blank=True, related_name='scheduling_manager')

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.title, self.association.name)



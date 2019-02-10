from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete

# Create your models here.


class RegistrationTemplate(models.Model):
    class Meta:
        verbose_name = "报名表模版"
        verbose_name_plural = "报名表模版表"
        app_label = 'interview'

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 标题
    title = models.CharField(max_length=255)

    # 版本号
    version = models.FloatField(default=0.0)

    # 附加信息
    additional = models.TextField(default='{}')

    # 启用与否
    using = models.BooleanField(default=False)

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "{}[{}] {}".format(self.association.name, self.version, self.title)


class Registration(models.Model):
    class Meta:
        verbose_name = "报名表"
        verbose_name_plural = "报名表"
        app_label = 'interview'

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 关联账户
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 版本号
    version = models.FloatField(default=0.0)

    # 名称
    realname = models.CharField(max_length=50)

    # 附加信息
    additional = models.TextField(default='{}')

    # 是否淘汰
    eliminate = models.BooleanField(default=False)

    def __str__(self):
        return "{}[{}] {}".format(self.association.name, self.version, self.realname)



@receiver(post_save, sender=RegistrationTemplate)
def version_selfadd(instance, **kwargs):
    """
    自增版本号
    :param instance:
    :param kwargs:
    :return:
    """
    if kwargs.get('create', False) is True:
        instance.version = RegistrationTemplate.objects.all().order_by('version')[-1] + 1
        instance.save()

@receiver(post_delete, sender=RegistrationTemplate)
def version_resort(instance, **kwargs):
    """
    重排版本号
    :param instance:
    :param kwargs:
    :return:
    """
    version = 1
    registration_template = RegistrationTemplate.objects.filter(association=instance.association).order_by('version')
    for template in registration_template:
        template.version = version
        version += 1
        template.save()


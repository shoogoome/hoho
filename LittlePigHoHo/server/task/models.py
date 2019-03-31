from django.db import models
from common.core.dao.cache.model_manager import HoHoModelManager
from common.core.dao.cache.factory import bind_model_cached_manager_signal
from common.core.dao.cache.factory import delete_model_single_object_cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from common.core.dao.time_stamp import TimeStampField



class AssociationTask(models.Model):
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务表"
        app_label = 'task'

    # 发起人
    author = models.ForeignKey('association.AssociationAccount', on_delete=models.CASCADE)

    # 关联协会
    association = models.ForeignKey('association.Association', on_delete=models.CASCADE)

    # 关联部门
    department = models.ForeignKey('association.AssociationDepartment', on_delete=models.CASCADE, blank=True, null=True)

    # 标题
    title = models.CharField(max_length=255)

    # 任务内容
    content = models.TextField(default="")

    # 开始时间
    start_time = models.FloatField(default=0.0)

    # 结束时间
    end_time = models.FloatField(default=0.0)

    # 是否正在进行
    working = models.BooleanField(default=False)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] 标题:{} 发起人:{}".format(self.id, self.title, self.author.nickname)


class AssociationTaskReport(models.Model):

    class Meta:
        verbose_name = "任务进度汇报"
        verbose_name_plural = "任务进度汇报表"
        app_label = 'task'

    # 关联关联
    task = models.ForeignKey('task.AssociationTask', on_delete=models.CASCADE)

    # 完成人
    worker = models.ForeignKey('association.AssociationAccount', blank=True, on_delete=models.SET_NULL, null=True)

    # 是否已完成
    complete = models.BooleanField(default=False)

    # 总结
    summary = models.TextField(default="")

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = HoHoModelManager()

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.task.title, self.worker.nickname)



receiver(post_save, sender=AssociationTask)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationTask)(delete_model_single_object_cache)

receiver(post_save, sender=AssociationTaskReport)(delete_model_single_object_cache)
receiver(post_delete, sender=AssociationTaskReport)(delete_model_single_object_cache)


from server.association.logic.info import AssociationLogic
from ..models import AssociationTask, AssociationTaskReport
from common.exceptions.task.info import TaskInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class TaskLogic(AssociationLogic):

    TASK_FIELD = [
        'author', 'author__id', 'author__nickname', 'association', 'association__id',
        'department', 'department__id', 'title', 'content', 'start_time', 'end_time',
        'working', 'update_time'
    ]

    TASK_REPORT_FIELD = [
        'task', 'task__id', 'worker', 'worker__id', 'summary',
        'create_time', 'update_time',
    ]

    def __init__(self, auth, sid, aid, tid="", trid=""):
        """
        任务模块逻辑
        :param auth:
        :param sid:
        :param aid:
        :param tid:
        :param trid:
        """
        super(TaskLogic, self).__init__(auth, sid, aid)

        if isinstance(tid, AssociationTask):
            self.task = tid
        else:
            self.task = self.get_task(tid)
        if isinstance(trid, AssociationTaskReport):
            self.task_report = trid
        else:
            self.task_report = self.get_task_report(trid)


    def get_task(self, tid):
        """
        获取任务表
        :param tid:
        :return:
        """
        if tid == "" or tid is None:
            return
        task = AssociationTask.objects.get_once(pk=tid)
        if task is None or task.association_id != self.association.id:
            raise TaskInfoExcept.no_task()

        return task

    def get_task_report(self, trid):
        """
        获取任务进度汇报
        :param trid:
        :return:
        """
        if trid == "" or trid is None:
            return
        task_report = AssociationTaskReport.objects.get_once(pk=trid)
        if task_report is None:
            raise TaskInfoExcept.no_task_report()

        return task_report

    def get_task_info(self):
        """
        获取任务表信息
        :return:
        """
        return model_to_dict(self.task, self.TASK_FIELD)

    def get_task_report_info(self):
        """
        获取任务进度汇报信息
        :return:
        """
        return model_to_dict(self.task_report, self.TASK_FIELD)




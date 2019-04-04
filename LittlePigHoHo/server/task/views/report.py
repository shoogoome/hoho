from ..models import AssociationTaskReport, AssociationTask
from ..logic.info import TaskLogic
from common.core.http.view import HoHoView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.models import AssociationDepartment
from common.exceptions.association.department import DepartmentExcept
from django.db.models import Q
from common.utils.helper.pagination import slicer
from server.association.models import AssociationAccount
from common.exceptions.association.info import AssociationExcept
from common.exceptions.task.info import TaskInfoExcept


class TaskReportView(HoHoView):


    def get(self, request, sid, aid, tid):
        """
        获取任务汇报情况
        :param request:
        :param sid:
        :param aid:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, sid, aid, tid)

        return Result(data=logic.get_task_report_info())

    def post(self, request, sid, aid, tid):
        """
        接手任务 or 指派任务
        :param request:
        :param sid:
        :param aid:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, sid, aid, tid)
        params = ParamsParser(request.JSON)
        account_id = params.int('account', desc='用户id', default=-1, require=False)

        if logic.task.working:
            raise TaskInfoExcept.working()

        # 指派任务
        if account_id != -1:
            account = AssociationAccount.objects.get_once(pk=account_id)
            # 过滤协会
            if account is None or account.association_id != logic.association.id:
                raise AssociationExcept.not_account()
        else:
            account = logic.account


        AssociationTaskReport.objects.create(
            task=logic.task,
            worker=account,
        )
        logic.task.working = True
        logic.task.save()

        return Result(id=tid)

    def put(self, request, sid, aid, tid):
        """
        完成任务
        :param request:
        :param sid:
        :param aid:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, sid, aid, tid)
        report = logic.task_report
        params = ParamsParser(request.JSON)

        if not logic.task.working:
            raise TaskInfoExcept.working()

        if params.has('summary'):
            report.summary = params.str('summary', desc='总结')
        report.complete = True

        report.save()
        return Result(id=tid)


    def delete(self, request, sid, aid, tid):
        """
        放弃任务
        :param request:
        :param sid:
        :param aid:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, sid, aid, tid)

        if not logic.task.working:
            raise TaskInfoExcept.working()
        logic.task_report.delete()
        logic.task.working = False
        logic.task.save()

        return Result(id=tid)













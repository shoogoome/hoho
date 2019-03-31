from ..models import AssociationTaskReport, AssociationTask
from ..logic.info import TaskLogic
from common.core.http.view import HoHoView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result



class TaskInfo(HoHoView):


    def get(self, request, sid, aid, tid):
        """
        获取任务表
        :param request:
        :param sid:
        :param aid:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, sid, aid, tid)

        return Result(logic.get_task_info())

    def post(self, request, sid, aid):
        """
        发布任务
        :param request:
        :param sid:
        :param aid:
        :return:
        """













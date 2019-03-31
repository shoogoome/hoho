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
        logic = TaskLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        title = params.str('title', desc='标题')
        content = params.str('content', desc='任务内容')
        start_time = params.float('start_time', desc='开始时间')
        end_time = params.float('end_time', desc='结束时间')
        department = params.int('department', desc='部门', require=False, default=-1)
        
        # 过滤协会
        if department != -1:
            if not AssociationDepartment.objects.filter(id=department, association_id=aid).exists():
                raise DepartmentExcept.department_not_found()

        task = AssociationTask.objects.create(
            title=title,
            content=content,
            start_time=start_time,
            end_time=end_time,
            author=logic.account,
            association_id=aid,
        )
        if department != -1:
            task.department_id = department
            task.save()
            
        return Result(id=task.id)
    
    
    def put(self, request, sid, aid, tid):
        """
        修改任务详情
        :param request: 
        :param sid: 
        :param aid: 
        :param tid: 
        :return: 
        """
        params = ParamsParser(request.JSON)
        logic = TaskLogic(self.auth, sid, aid, tid)
        task = logic.task
        
        with params.diff(task):
            task.title = params.str('title', desc='标题')
            task.content = params.str('content', desc='任务内容')
            task.start_time = params.float('start_time', desc='开始时间')
            task.end_time = params.float('end_time', desc='结束时间')
        task.save()

        return Result(id=tid)

    def delete(self, request, sid, aid, tid):
        """
        删除任务
        :param request:
        :param sid:
        :param aid:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, sid, aid, tid)

        logic.task.delete()
        return Result(id=tid)


class TaskView(HoHoView):

    def get(self, request, sid, aid):
        """
        获取任务列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)
        
        tasks = AssociationTask.objects.values('id', 'update_time').filter(association_id=aid)
        if params.has('key'):
            key = params.str('key', desc='关键字 标题 内容')
            tasks = tasks.filter(
                Q(title__contains=key) |
                Q(content__contains=key)
            )

        if params.has('working'):
            tasks = tasks.filter(working=params.bool('working', desc='是否以被接任务'))

        if params.has('start_time'):
            tasks = tasks.filter(start_time__gte=params.float('start_time', desc='开始时间'))

        if params.has('end_time'):
            tasks = tasks.filter(end_time__lte=params.float('end_time', desc='结束时间'))

        if params.has('department'):
            tasks = tasks.fiter(department_id=params.int('department', desc='部门id'))

        @slicer(tasks, limit=limit, page=page)
        def get_tasks_list(obj):
            return obj

        tasks, pagination = get_tasks_list()
        return Result(tasks=tasks, pagination=pagination)


    def post(self, request, sid, aid):
        """
        批量获取任务信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = TaskLogic(self.auth, sid, aid)
        ids = params.list('ids', desc='id列表')

        tasks = AssociationTask.objects.get_many(ids=ids)

        data = []
        for task in tasks:
            try:
                logic.task = task
                data.append(logic.get_task_info())
            except:
                pass

        return Result(data)
from django.db.models import Q

from common.core.http.view import HoHoView
from common.exceptions.association.department import DepartmentExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.models import AssociationDepartment
from ..logic.notice import NoticeLogic
from ..models import AssociationNotice


class NoticeInfo(HoHoView):

    def get(self, request, sid, aid, nid):
        """
        获取通知信息
        :param request:
        :param sid:
        :param aid:
        :param nid:
        :return:
        """
        logic = NoticeLogic(self.auth, sid, aid, nid)

        return Result(logic.get_notice_info())

    def post(self, request, sid, aid):
        """
        创建通知信息  协会 or 部门
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        title = params.str('title', desc='标题')
        content = params.str('content', desc='正文')
        start_time = params.float('start_time', desc='开始时间')
        end_time = params.float('end_time', desc='结束时间')

        if params.has('department'):
            department = params.int('department', desc='部门id')
            if not AssociationDepartment.objects.filter(association_id=aid, id=department).exists():
                raise DepartmentExcept.department_not_found()

        notice = AssociationNotice.objects.create(
            title=title,
            content=content,
            start_time=start_time,
            end_time=end_time,
            author=self.auth.get_account(),
            association_id=aid,
        )
        if params.has('department'):
            notice.department_id = department

        return Result(id=notice.id)

    def put(self, request, sid, aid, nid):
        """
        修改通知信息
        :param request:
        :param sid:
        :param aid:
        :param nid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = NoticeLogic(self.auth, sid, aid, nid)
        notice = logic.notice

        with params.diff(notice):
            notice.title = params.str('title', desc='标题')
            notice.content = params.str('content', desc='正文')
            notice.start_time = params.float('start_time', desc='开始时间')
            notice.end_time = params.float('end_time', desc='结束时间')

        notice.save()

        return Result(id=nid)

    def delete(self, auth, sid, aid, nid):
        """
        删除通知信息
        :param auth:
        :param sid:
        :param aid:
        :param nid:
        :return:
        """
        logic = NoticeLogic(self.auth, sid, aid, nid)
        logic.notice.delete()

        return Result(id=nid)


class NoticeView(HoHoView):

    def get(self, request, sid, aid):
        """
        获取通知列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        notice = AssociationNotice.objects.values('id', 'update_time').filter(association_id=aid)
        if params.has('key'):
            key = params.str('key', desc='关键字')
            notice = notice.filter(
                Q(title__contains=key) |
                Q(content__contains=key)
            )

        if params.has('start_time'):
            notice = notice.filter(start_time__gte=params.float('start_time', desc='开始时间'))

        if params.has('end_time'):
            notice = notice.filter(end_time__lte=params.float('end_time', desc='结束时间'))

        if params.has('department'):
            notice = notice.filter(department_id=params.int('department', desc='协会id'))

        @slicer(notice, limit=limit, page=page)
        def get_notice_list(obj):
            return obj

        notices, pagination = get_notice_list()
        return Result(notices=notices, pagination=pagination)

    def post(self, request, sid, aid):
        """
        批量获通知信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = NoticeLogic(self.auth, sid, aid)

        ids = params.list('ids', desc='通知id列表')
        notices = AssociationNotice.objects.get_many(ids=ids)

        data = list()
        for notice in notices:
            try:
                logic.notice = notice
                data.append(logic.get_notice_info())
            except:
                pass

        return Result(data)

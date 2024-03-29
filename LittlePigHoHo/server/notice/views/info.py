from django.db.models import Q

from common.core.http.view import HoHoView
from common.exceptions.association.department import DepartmentExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.models import AssociationDepartment
from ..logic.notice import NoticeLogic
from common.core.auth.check_login import check_login
from ..models import AssociationNotice
from common.enum.association.permission import AssociationPermissionEnum
from common.enum.account.role import RoleEnum

class NoticeInfo(HoHoView):

    @check_login
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

        return Result(data=logic.get_notice_info(), association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        创建通知信息  协会 or 部门
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = NoticeLogic(self.auth, sid, aid)
        # logic.check(AssociationPermissionEnum.NOTICE)

        params = ParamsParser(request.JSON)
        title = params.str('title', desc='标题')
        content = params.str('content', desc='正文')
        start_time = params.float('start_time', desc='开始时间')
        end_time = params.float('end_time', desc='结束时间')

        if logic.account.role == int(RoleEnum.DIRECTOR):
            raise DepartmentExcept.no_permission()

        notice = AssociationNotice.objects.create(
            title=title,
            content=content,
            start_time=start_time,
            end_time=end_time,
            author=logic.account,
            association_id=aid,
        )
        if logic.account.role == int(RoleEnum.MINISTER):
            depertment = AssociationDepartment.objects.filter(manager=logic.account)
            if not depertment.exists():
                notice.delete()
                raise DepartmentExcept.no_affiliated_department()
            notice.department = depertment[0]
            notice.save()

        return Result(id=notice.id, association_id=self.auth.get_association_id())

    @check_login
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
        # logic.check(AssociationPermissionEnum.NOTICE)
        notice = logic.notice

        with params.diff(notice):
            notice.title = params.str('title', desc='标题')
            notice.content = params.str('content', desc='正文')
            notice.start_time = params.float('start_time', desc='开始时间')
            notice.end_time = params.float('end_time', desc='结束时间')

        notice.save()

        return Result(id=nid, association_id=self.auth.get_association_id())

    @check_login
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
        # logic.check(AssociationPermissionEnum.NOTICE)
        logic.notice.delete()

        return Result(id=nid, association_id=self.auth.get_association_id())


class NoticeView(HoHoView):

    @check_login
    def get(self, request, sid, aid):
        """
        获取通知列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = NoticeLogic(self.auth, sid, aid)
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        notice = AssociationNotice.objects.values('id', 'update_time').filter(association_id=aid).order_by('-create_time')
        if params.has('key'):
            key = params.str('key', desc='关键字 标题 正文')
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

        notice = list(notice)
        notice.extend(logic.get_remember())
        @slicer(notice, limit=limit, page=page)
        def get_notice_list(obj):
            return obj

        notices, pagination = get_notice_list()
        return Result(notices=notices, pagination=pagination, association_id=self.auth.get_association_id())

    @check_login
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
                if logic.notice.association_id != logic.association.id:
                    continue
                data.append(logic.get_notice_info())
            except:
                pass

        return Result(data=data, association_id=self.auth.get_association_id())

class NoticeRememberView(HoHoView):


    @check_login
    def post(self, request, sid, aid):
        """
        批量记住通知
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = NoticeLogic(self.auth, sid, aid)

        params = ParamsParser(request.JSON)
        ids = params.list("ids", desc="通知id列表")

        static = {}
        notices = AssociationNotice.objects.get_many(ids=ids)
        for notice in notices:

            logic.notice = notice
            if logic.notice.association_id != logic.association.id:
                _static = -1
            else:
                _static = 1 if logic.remember() else 0
            static[str(notice.id)] = _static

        return Result(static=static)

    @check_login
    def get(self, request, sid, aid, nid):
        """
        记住通知
        :param request:
        :param sid:
        :param aid:
        :param nid:
        :return:
        """
        logic = NoticeLogic(self.auth, sid, aid, nid)
        _static = logic.remember()

        return Result(static = _static)


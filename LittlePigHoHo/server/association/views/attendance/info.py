from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.entity.association.backlog import AssociationBacklog
from common.exceptions.association.attendance import AttendanceExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.logic.attendance import AttendanceLogic
from server.association.logic.info import AssociationLogic
from server.association.models import AssociationAttendance


class AttendanceView(HoHoView):

    @check_login
    def get(self, request, sid, aid, vid):
        """
        获取考勤表信息
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, aid, vid)

        return Result(data=logic.get_attendance_info(), association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        创建考勤记录
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)

        title = params.str('title', desc='标题')
        place_x = params.float('place_x', desc='纬度')
        place_y = params.float('place_y', desc='经度')
        distance = params.float('distance', desc='容错距离', require=False, default=100.0)
        start_time = params.float('start_time', desc='开始时间')
        end_time = params.float('end_time', desc='结束时间')

        # 过滤标题
        if AssociationAttendance.objects.filter(association=logic.association, title=title).exists():
            raise AttendanceExcept.title_exist()

        association = AssociationAttendance.objects.create(
            title=title,
            author=logic.account,
            association=logic.association,
            description=params.str('description', desc='描述', require=False, default=""),
            place_x=place_x,
            place_y=place_y,
            distance=distance,
            start_time=start_time,
            end_time=end_time,
        )

        return Result(id=association.id, association_id=self.auth.get_association_id())

    @check_login
    def put(self, request, sid, aid, vid):
        """
        修改考勤记录
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, aid, vid)
        params = ParamsParser(request.JSON)
        attendance = logic.attendance

        # 过滤标题
        if params.has('title'):
            title = params.str('title', desc='标题')
            if AssociationAttendance.objects.filter(association=logic.association, title=title).exists():
                raise AttendanceExcept.title_exist()

        with params.diff(attendance):
            attendance.description = params.str('description', desc='描述')
            attendance.place_x = params.float('place_x', desc='考勤纬度')
            attendance.place_y = params.float('place_y', desc='考勤经度')
            attendance.distance = params.float('distance', desc='容错距离')
            attendance.start_time = params.float('start_time', desc='开始时间')
            attendance.end_time = params.float('end_time', desc='结束时间')

        attendance.save()
        return Result(id=vid, association_id=self.auth.get_association_id())

    @check_login
    def delete(self, request, sid, aid, vid):
        """
        删除考勤记录
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, aid, vid)

        logic.attendance.delete()
        return Result(id=vid, association_id=self.auth.get_association_id())


class AttendanceInfo(HoHoView):

    @check_login
    def get(self, request, sid, aid):
        """
        获取考勤列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        attendances = AssociationAttendance.objects.values('id', 'update_time').filter(association__id=aid)

        if params.has('title'):
            attendances = attendances.filter(title__contains=params.str('title', desc='标题'))
        if params.has('start_time'):
            attendances = attendances.filter(start_time__gte=params.float('start_time', desc='开始时间'))
        if params.has('end_time'):
            attendances = attendances.filter(end_time__lte=params.float('end_time', desc='结束时间'))

        @slicer(attendances, limit=limit, page=page)
        def get_attendances_list(obj):
            return obj

        attendances, pagination = get_attendances_list()
        return Result(attendances=attendances, pagination=pagination, association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        批量获取协会考勤信息
        :param request:
        :param sid:
        :param aid:
        :return:  -1-尚未开始 0-已经结束 1-正在进行
        """
        params = ParamsParser(request.JSON)
        logic = AttendanceLogic(self.auth, sid, aid)
        ids = params.list('ids', desc='考勤表id')

        data = list()
        attendances = AssociationAttendance.objects.get_many(ids=ids)
        for attendance in attendances:
            logic.attendance = attendance
            try:
                data.append(logic.get_attendance_info())
            except:
                pass

        return Result(data=data, association_id=self.auth.get_association_id())


class AttendanceSign(HoHoView):

    @check_login
    def get(self, request, sid, aid, vid):
        """
        签到
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        params = ParamsParser(request.GET)
        lx = params.float('lx', desc='纬度')
        ly = params.float('ly', desc='经度')
        logic = AttendanceLogic(self.auth, sid, aid, vid)
        logic.sign_or_leave(lxy=(lx, ly))

        return Result(id=vid, association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid, vid):
        """
        获取考勤情况
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, aid, vid)
        params = ParamsParser(request.JSON)
        _type = params.int('type', desc='考勤类别', default=0, require=False)   # type: int 0-协会 1-部门 2-个人

        if _type == 0:
            data = logic.get_association_sign_info()
        elif _type == 1:
            data = logic.get_department_sign_info(params.int('department', desc='部门id'))
        elif _type == 2:
            data = logic.get_account_sign_info()

        return Result(data=data, association_id=self.auth.get_association_id())


class AttendanceManage(HoHoView):

    @check_login
    def get(self, request, sid, aid, vid):
        """
        发起请假
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        params = ParamsParser(request.GET)
        alogic = AttendanceLogic(self.auth, sid, aid, vid)
        # 获取协会待办事项
        description = params.str('description', desc='请假事由')
        backlog = AssociationBacklog.parse(alogic.association.backlog)
        # key: [人事id][考勤表id] = 请假事由
        backlog.attendance[str(alogic.account.id)][str(vid)] = description
        # 更新数据库
        alogic.association.backlog = backlog.dumps()
        alogic.association.save()

        return Result(id=vid, association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid, vid):
        """
        处理考勤请假
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return: 0-无此人物待办事项 1-成功
        """
        alogic = AttendanceLogic(self.auth, sid, aid, vid)
        # 获取待办事项
        backlog = AssociationBacklog.parse(alogic.association.backlog)
        params = ParamsParser(request.JSON)

        data = params.dict('data', desc='处理情况')
        result = {}
        for aid in data:
            # 不存在该账户
            if backlog.attendance.get(aid, None) is None:
                result[aid] = 0
                continue
            # 删除kv
            del backlog.attendance[str(aid)][str(vid)]
            # redis缓存更新
            alogic.sign_or_leave(leave=(True, aid))
            result[aid] = 1
        # 更新数据库
        alogic.association.backlog = backlog.dumps()
        alogic.association.save()

        return Result(status=result, association_id=self.auth.get_association_id())

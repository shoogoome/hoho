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
from common.enum.association.permission import AssociationPermissionEnum
import time
from common.enum.account.role import RoleEnum
from ...logic.redis import AttendanceRedisFactory
from django.db.models import Q

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
        redis = AttendanceRedisFactory()
        logic = AttendanceLogic(self.auth, sid, aid, vid)
        info = logic.get_attendance_info()
        _deparment_id = "-1" if logic.account.department is None else logic.account.department_id
        _aid = logic.account.id
        _status = redis.hget(
            logic.build_key(logic.attendance.id, _deparment_id),
            _aid
        )
        if _status is None:
            _status = -1
        info["attendance_status"] = _status
        return Result(data=info, association_id=self.auth.get_association_id())

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
        # logic.check(AssociationPermissionEnum.ATTENDANCE)
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
        _department = logic.account.department
        if logic.account.role == int(RoleEnum.MINISTER) and _department is not None:
            association.department = _department

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
        # logic.check(AssociationPermissionEnum.ATTENDANCE)
        params = ParamsParser(request.JSON)
        attendance = logic.attendance

        # 过滤标题
        if params.has('title'):
            title = params.str('title', desc='标题')
            if AssociationAttendance.objects.filter(title=title, association=logic.association).exclude(id=attendance.id).exists():
                raise AttendanceExcept.title_exist()
            attendance.title = title

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
        # logic.check(AssociationPermissionEnum.ATTENDANCE)

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
        logic = AssociationLogic(self.auth, sid, aid)

        attendances = AssociationAttendance.objects.values('id', 'update_time').filter(association__id=aid).filter(
            Q(department__isnull=True) |
            Q(department=logic.account.department)
        )
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
        redis = AttendanceRedisFactory()
        params = ParamsParser(request.JSON)
        logic = AttendanceLogic(self.auth, sid, aid)
        ids = params.list('ids', desc='考勤表id')

        data = list()
        attendances = AssociationAttendance.objects.get_many(ids=ids)
        _deparment_id = "-1" if logic.account.department is None else logic.account.department_id
        _aid = logic.account.id
        for attendance in attendances:
            logic.attendance = attendance
            try:
                info = logic.get_attendance_info()
                _status = redis.hget(
                    logic.build_key(logic.attendance.id, _deparment_id),
                    _aid
                )
                if _status is None:
                    _status = -1
                info["attendance_status"] = _status
                data.append(info)
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
        logic = AttendanceLogic(self.auth, sid, aid, vid)
        # logic.check(AssociationPermissionEnum.ATTENDANCE_SIGN)
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

        data = {}
        if _type == 2:
            data = logic.get_account_sign_info()
        else:
            # logic.check(AssociationPermissionEnum.ATTENDANCE)
            if _type == 0:
                data = logic.get_association_sign_info()
            elif _type == 1:
                data = logic.get_department_sign_info(params.int('department', desc='部门id'))

        return Result(data=data, association_id=self.auth.get_association_id())


class AttendanceManage(HoHoView):

    @check_login
    def post(self, request, sid, aid, vid):
        """
        发起请假
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        params = ParamsParser(request.JSON)
        alogic = AttendanceLogic(self.auth, sid, aid, vid)
        # if alogic.attendance.end_time < time.time():
        #     raise AttendanceExcept.no_in_place()
        # 获取协会待办事项
        description = params.str('description', desc='请假事由')
        backlog = AssociationBacklog.parse(alogic.association.backlog)
        # key: [人事id][考勤表id] = 请假事由
        _attendance = backlog.attendance()

        if str(vid) in _attendance:
            if str(alogic.account.id) in _attendance[str(vid)]["data"]:
                _attendance[str(vid)]["data"][str(alogic.account.id)]["description"] = description
            else:
                _attendance[str(vid)]["data"][str(alogic.account.id)] = {
                        "name": alogic.account.nickname,
                        "description": description
                }
        else:
            _attendance[str(vid)] = {
                "name": alogic.attendance.title,
                "data": {
                    str(alogic.account.id): {
                        "name": alogic.account.nickname,
                        "description": description
                    }
                }
            }

        """
                {
                    attendance: {
                        "考勤id": {
                            "name": "考勤名字",
                            "data": {
                                "人id": {
                                    "name": "名字",
                                    "description": "请假事由"
                                }
                            }
                        }
                    }
                }
        """

        backlog.attendance = _attendance
        # 更新数据库
        alogic.association.backlog = backlog.dumps()
        alogic.association.save()

        return Result(id=vid, association_id=self.auth.get_association_id())

class AttendanceManager(HoHoView):

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
        # alogic.check(AssociationPermissionEnum.ATTENDANCE)
        # 获取待办事项
        backlog = AssociationBacklog.parse(alogic.association.backlog)
        # backlog = backlog.dump()
        params = ParamsParser(request.JSON)

        data = params.dict('data', desc='处理情况')
        result = {}

        attendance = backlog.attendance()
        if str(vid) not in backlog.attendance():
            return Result(status=result)

        for aid, vl in data.items():
            if str(aid) in attendance[str(vid)]["data"] and vl:
                if vl:
                    alogic.sign_or_leave(leave=(True, str(aid)))
                del attendance[str(vid)]["data"][str(aid)]

            # redis缓存更新
            alogic.sign_or_leave(leave=(True, aid))
            result[aid] = 1
        # 更新数据库
        backlog.attendance = attendance
        alogic.association.backlog = backlog.dumps()
        alogic.association.save()

        return Result(status=result, association_id=self.auth.get_association_id())



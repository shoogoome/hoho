import time
import json

from common.core.auth.check_login import check_login
from common.core.dao.redis import get_redis_conn
from common.core.http.view import HoHoView
from common.enum.association.permission import AssociationPermissionEnum
from common.utils.helper.m_t_d import model_to_dict
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.attendance import AttendanceLogic
from ..logic.info import AssociationLogic
from common.exceptions.association.attendance import AttendanceExcept
from ..models import AssociationAttendance
from common.entity.association.backlog import AssociationBacklog

class AttendanceView(HoHoView):
    NOMAL_FILE = [
        'title', 'author', 'description', 'place', 'start_time', 'end_time', 'version'
    ]

    @check_login
    def post(self, request, sid, aid):
        """
        创建考勤记录
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        alogic = AssociationLogic(self.auth, sid, aid)
        alogic.check(AssociationPermissionEnum.ATTENDANCE_CREATE)

        params = ParamsParser(request.JSON)

        association = AssociationAttendance.objects.create(
            title=params.str('title', desc='考勤标题'),
            author=self.auth.get_account(),
            association=alogic.association,
            description=params.str('description', desc='描述', require=False, default=""),
            place=params.str('place', desc='地点', require=False, default=""),
            start_time=params.float('start_time', desc='开始时间'),
            end_time=params.float('end_time', desc='结束时间')
        )

        _ass = AssociationAttendance.objects.filter(association=alogic.association).order_by('-version')
        association.version = _ass[0].version + 1 if _ass.exists() else 1
        association.save()

        return Result(id=association.id)

    @check_login
    def get(self, request, sid, aid):
        """
        获取协会考勤表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        alogic = AssociationLogic(self.auth, sid, aid)
        _time = time.time()

        data = list()
        for att in alogic.filter_attendance():
            try:
                status = 1
                result = model_to_dict(att, self.NOMAL_FILE)
                if _time > result.get('end_time', 0):
                    status = 0
                elif _time < result.get('start_time', 0):
                    status = -1
                result['status'] = status
                data.append(result)
            except:
                pass

        return Result(data)


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
        redis = get_redis_conn()
        alogic = AttendanceLogic(self.auth, sid, aid, vid)
        alogic.check(AssociationPermissionEnum.ATTENDANCE)

        try:
            redis.setbit(
                name="{0}_{1}[version:{2}]_{3}".format(
                    alogic.assocation.name,
                    alogic.attendance.title,
                    alogic.attendance.version,
                    str(self.auth.get_account().id),
                ),
                offset=0,
                value=True
            )
        except:
            pass

        return Result(id=self.auth.get_account().id)

    @check_login
    def post(self, request, sid, aid, vid):
        """
        获取签到情况
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        redis = get_redis_conn()
        alogic = AttendanceLogic(self.auth, sid, aid, vid)
        alogic.check(AssociationPermissionEnum.ATTENDANCE.ATTENDANCE_VIEW)

        ids = [str(_ass.id) for _ass in alogic.assocation.account_set.all()]
        _name = "{0}_{1}[version:{2}]_".format(
            alogic.assocation.name,
            alogic.attendance.title,
            alogic.attendance.version,
        )

        result = dict()
        for _id in ids:
            status = 0
            if redis.getbit(name=_name + _id, offset=0):
                status = 1
            elif redis.getbit(name=_name + _id, offset=1):
                status = 2
            result[_id] = status
        return Result(status=result)

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
        if alogic.attendance.end_time < time.time():
            raise AttendanceExcept.time_out()

        description = params.str('description', desc='请假事由')
        backlog = AssociationBacklog.parse(alogic.assocation.backlog).dump()

        backlog['attendance'][str(self.auth.get_account().id)] = description

        alogic.assocation.backlog = json.dumps(backlog)
        alogic.assocation.save()

        return Result(id=self.auth.get_account().id)

    @check_login
    def post(self, request, sid, aid, vid):
        """
        处理考勤请假
        :param request:
        :param sid:
        :param aid:
        :param vid:
        :return:
        """
        redis = get_redis_conn()
        alogic = AttendanceLogic(self.auth, sid, aid, vid)
        alogic.check(AssociationPermissionEnum.ATTENDANCE_MANAGE)

        backlog = AssociationBacklog.parse(alogic.assocation.backlog).dump()
        params = ParamsParser(request.JSON)

        data = params.dict('data', desc='处理情况')
        """{"id": true or false}"""

        _name = "{0}_{1}[version:{2}]_".format(
            alogic.assocation.name,
            alogic.attendance.title,
            alogic.attendance.version)
        result = {}
        for aid in data:
            if backlog['attendance'].get(aid, None) is None:
                result[aid] = 0
                continue
            del backlog['attendance'][aid]

            redis.setbit(
                name=_name + aid,
                offset=1,
                value=True
            )

            result[aid] = 1
        alogic.assocation.backlog = json.dumps(backlog)
        alogic.assocation.save()

        return Result(status=result)

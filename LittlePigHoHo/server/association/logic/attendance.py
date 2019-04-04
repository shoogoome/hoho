import json
import time

from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.exceptions.association.attendance import AttendanceExcept
from common.exceptions.association.info import AssociationExcept
from server.school.logic.info import SchoolLogic
from server.school.models import School
from ..logic.info import AssociationLogic
from ..models import Association
from ..models import AssociationAttendance
from ..logic.info import AssociationLogic
from common.core.dao.redis import get_redis_conn
from ..models import AssociationAccount
from common.utils.helper.m_t_d import model_to_dict
from ..models import AssociationDepartment
from math import *
from .redis import AttendanceRedisFactory


class AttendanceLogic(AssociationLogic):

    EARTH_REDIUS = 6378.137

    NOMAL_FILE = [
        'title', 'author', 'author__id', 'author__nickname', 'description',
        'start_time', 'end_time', 'distance', 'place_y', 'place_x',
    ]

    def __init__(self, auth, sid, aid, atid=''):
        """
        考勤逻辑
        :param auth:
        :param sid:
        :param aid:
        :param atid:
        """
        super(AttendanceLogic, self).__init__(auth, sid, aid)

        if isinstance(atid, AssociationAttendance):
            self.attendance = atid
        else:
            self.attendance = self.get_attendance(atid)

        self.redis = None
        self.name = self.association.id
        self.department_id = self.account.department_id if self.association.colony else '-1'


    def get_attendance(self, atid):
        """
        获取attendance
        :param atid:
        :return:
        """
        if atid == "" or atid is None:
            return None
        attendance = AssociationAttendance.objects.get_once(pk=atid)
        if attendance is not None or attendance.association_id != self.association.id:
            return attendance

        raise AttendanceExcept.attendance_not_found()

    def get_attendance_info(self):
        """
        获取考勤表信息
        :return:
        """
        _time = time.time()
        info = model_to_dict(self.attendance, self.NOMAL_FILE)
        # 记录状态
        status = 1
        if _time > info.get('end_time', 0):
            status = 0
        elif _time < info.get('start_time', 0):
            status = -1
        info['status'] = status

        return info


    def sign_or_leave(self, lxy=(0, 0), leave=(False, "")):
        """
        签到 or 请假
        Redis key格式
        " attendance: 协会id: 考勤表id: 部门id(没有则-1)
        key 人事表id: value 1-签到 0-请假"
        :param lxy
        :param leave:
        :return:
        """
        if self.redis is None:
            self.redis = AttendanceRedisFactory()
        account_id = leave[1] if leave[0] else self.account.id

        # 签到判断距离
        if not leave:
            # 超过容错距离
            if AttendanceLogic.distance(*lxy, self.attendance.place_x, self.attendance.place_y) > self.attendance.distance:
                raise AttendanceExcept.no_in_place()

        self.redis.hset(
            self._build_key(self.attendance.id, self.department_id),
            account_id,
            0 if leave[0] else 1
        )


    def get_account_sign_info(self, account_id="", department_id="-1"):
        """
        获取用户签到情况
        :param account_id:
        :param department_id:
        :return:
        """
        if self.redis is None:
            self.redis = AttendanceRedisFactory()

        if account_id == "" or account_id is None:
            status = self.redis.hget(
                self._build_key(self.attendance.id, self.department_id),
                self.account.id
            )
        else:
            status = self.redis.hget(
                self._build_key(self.attendance.id, department_id),
                account_id
            )
        return status


    def get_department_sign_info(self, department_id, ass=False):
        """
        获取部门签到情况
        :param department_id:
        :return:
        """
        if self.redis is None:
            self.redis = AttendanceRedisFactory()

        status = {}
        if not ass:
            status = {str(aid['id']): -1 for aid in AssociationAccount.objects.values('id').filter(association=self.association, retire=False, department_id=department_id)}
        _status = self.redis.hgetall(
                self._build_key(self.attendance.id, department_id)
            )
        for k, v in _status.items():
            status[k.decode()] = v.decode()

        return status


    def get_association_sign_info(self):
        """
        获取协会签到情况
        :return:
        """
        if not self.association.colony:
            return self.get_department_sign_info('-1')

        # 获取全部部门
        department_id = AssociationDepartment.objects.values('id').filter(association=self.association)

        account = AssociationAccount.objects.values('id').filter(association=self.association, retire=False)
        status = {}
        for did in department_id:
            status[str(did)] = {str(aid['id']): -1 for aid in account.filter(department_id=did)}
            status[str(did)].update(self.get_department_sign_info(str(did), ass=True))

        return status


    def get_range_sign_info(self, start_time, end_time):
        """
        获取区间内签到情况
        :param start_time:
        :param end_time:
        :return:
        """
        if self.redis is None:
            self.redis = AttendanceRedisFactory()

        # 获取在任人员
        account_ids = AssociationAccount.objects.values('id').filter(association=self.association, retire=False)
        # 获取考勤总数
        attendance_ids = AssociationAttendance.objects.values('id').filter(start_time__gte=start_time, end_time__lte=end_time)
        # 获取全部部门
        department_ids = AssociationDepartment.objects.values('id').filter(association=self.association)


        status = {"total": attendance_ids.count()}     # type: dict {"id": ["请假次数", "签到次数", "缺席次数"]}
        # 遍历考勤
        for attendance_id in attendance_ids:
            if self.association.colony:
                # 遍历部门
                for department_id in department_ids:
                    _status = self.redis.hgetall(self._build_key(attendance_id['id'], department_id))
                    # 写入计数
                    for account_id in account_ids.filter(department_id=department_id):
                        account_id = account_id['id']
                        if str(account_id) in status:
                            status[str(account_id)][int(_status.get(str(account_id).encode(), b'-1').decode())] += 1
                        else:
                            status[str(account_id)] = [0, 0, 0]
                            status[str(account_id)][int(_status.get(str(account_id).encode(), b'-1').decode())] = 1
            else:
                _status = self.redis.hgetall(self._build_key(attendance_id['id'], '-1'))
                # 写入计数
                for account_id in account_ids:
                    account_id = account_id['id']
                    if str(account_id) in status:
                        status[str(account_id)][int(_status.get(str(account_id).encode(), b'-1').decode())] += 1
                    else:
                        status[str(account_id)] = [0, 0, 0]
                        status[str(account_id)][int(_status.get(str(account_id).encode(), b'-1').decode())] = 1

        return status

    def _build_key(self, *args):
        """
        构建key
        :param key:
        :return:
        """
        return ":".join([str(i) for i in [self.name, *args]])

    @staticmethod
    def distance(lna, laa, lnb, lab):
        """
        计算经纬度之间距离
        :param lna:
        :param laa:
        :param lnb:
        :param lab:
        :return:  米为单位的距离
        """
        ra = 6378.140  # 赤道半径
        rb = 6356.755  # 极半径 （km）
        flatten = (ra - rb) / ra  # 地球偏率
        rad_lat_a = radians(laa)
        rad_lng_a = radians(lna)
        rad_lat_b = radians(lab)
        rad_lng_b = radians(lnb)
        pA = atan(rb / ra * tan(rad_lat_a))
        pB = atan(rb / ra * tan(rad_lat_b))
        xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_a - rad_lng_b))
        c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
        c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (xx + dr)
        return distance * 1000




    # def check(self, *permission):
    #     """
    #     权限处理
    #     :param permission:
    #     :return:
    #     """
    #     if self.auth.get_account().role == int(RoleEnum.ADMIN):
    #         return True
    #
    #     if not AttendanceLogic.inspect(self.auth.get_account(), self.assocation,
    #                                    self.attendance, self.association_logic.ass_acc, *permission):
    #         raise AssociationExcept.no_permission()
    #
    # @staticmethod
    # def inspect(account, association, attendance, ass_acc=None, *permission):
    #     """
    #     权限判断
    #     :param account:
    #     :param association:
    #     :param attendance:
    #     :param ass_acc:
    #     :param permission:
    #     :return:
    #     """
    #     a_permission = json.loads(account.permissions)
    #     ass_permission = json.loads(association.configure)
    #
    #     _att = ass_permission.get('attendance', dict())
    #     _end = attendance.end_time
    #     _start = attendance.start_time
    #     _manage = account.id in ass_permission.get('manage', [])
    #
    #     if AssociationPermissionEnum.ATTENDANCE in permission:
    #         if association in account.association.all():
    #             if _start <= time.time() <= _end:
    #                 return True
    #
    #     # 判断管理员权限
    #     if _manage or (ass_acc.role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]):
    #         return True
    #
    #     # 检查考勤权限
    #     if _att is dict():
    #         return False
    #
    #     if AssociationPermissionEnum.ATTENDANCE_VIEW in permission:
    #         if account.id in _att.get('views', list()):
    #             return True
    #
    #     if AssociationPermissionEnum.ATTENDANCE_MANAGE in permission:
    #         if account.id in _att.get('manage', list()):
    #             return True
    #
    #     return False

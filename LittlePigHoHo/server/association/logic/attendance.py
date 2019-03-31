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


class AttendanceLogic(AssociationLogic):

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

        self.name = "attendance:{}".format(self.association.id)
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


    def sign_or_leave(self, leave=False, account_id=""):
        """
        签到 or 请假
        Redis key格式
        " attendance: 协会id: 部门id(没有则-1): 考勤表id: 人事表id: 1-签到 0-请假 "
        :param leave:
        :param account_id:
        :return:
        """
        redis = get_redis_conn()

        account = self.account
        # 构建key
        key = "{0}:{1}:{2}:{3}".format(self.department_id, self.attendance.id, str(account_id) if leave else account.id, '0' if leave else '1')
        # 以开始为score
        redis.zadd(self.name, {
            key: self.attendance.start_time
        })

    def get_range_sign_info(self, start_time, end_time, account=False, department=False):
        """
        获取区间内签到情况
        :param start_time:
        :param end_time:
        :param account:
        :param department:
        :return:
        """
        redis = get_redis_conn()

        # 获取全部部门
        department_id = AssociationDepartment.objects.values('id').filter(association=self.association)
        # 获取在任人员
        account_ids = AssociationAccount.objects.values('id').filter(association=self.association, retire=False)
        # 获取考勤总数
        attendance_ids = AssociationAttendance.objects.values('id').filter(start_time__gte=start_time, end_time__lte=end_time)
        status_list = redis.zrangebyscore(
            name=self.name,
            min=start_time,
            max=end_time,
        )

        _status = {
            "total": attendance_ids.count()
        }
        for s in status_list:
            # 0号位为部门id 1号位为考勤表id 2号位为用户id 3号位为状态 1-签到 0-请假
            s = s.decode().split(':')
            _s = int(s[3])
            if not account:
                # 部门优先模式
                if department:
                    if s[0] in _status:
                        _status[s[0]][s[1]][s[2]] = _s
                    else:
                        _status = {str(did['id']): {str(atid['id']): {str(aid['id']): -1 for aid in account_ids} for atid in attendance_ids} for did in department_id}
                        _status[s[0]][s[1]][s[2]] = _s
                else:
                    # 考勤id记录已存在则直接记录
                    if s[1] in _status:
                        _status[s[1]][s[2]] = _s
                    # 考勤id记录不存在则初始化
                    else:
                        _status = {str(atid['id']): {str(aid['id']): -1 for aid in account_ids} for atid in attendance_ids}
                        _status[s[1]][s[2]] = _s
            else:
                # 账户id记录已存在则直接记录
                if s[2] in _status:
                    _status[s[2]][s[1]] = _s
                # 账户id记录不存在则初始化
                else:
                    _status = {str(aid['id']): {str(atid['id']): -1 for atid in attendance_ids} for aid in account_ids}
                    _status[s[2]][s[1]] = _s

        return _status


    def _build_key(self, *args):
        """
        构建key
        :param key:
        :return:
        """
        return ":".join([self.name, *args])



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

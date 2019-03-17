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


class AttendanceLogic(object):

    def __init__(self, auth, sid, asid, atid='', is_version=False):
        """
        INIT
        :param auth:
        :param sid:
        :param asid:
        :param atid:
        :param is_version:
        """
        self.auth = auth

        if isinstance(sid, SchoolLogic):
            self.schoolLogic = sid
            self.school = sid.school
        elif isinstance(sid, School):
            self.schoolLogic = SchoolLogic(self.auth, sid)
            self.school = sid
        else:
            self.schoolLogic = SchoolLogic(self.auth, sid)
            self.school = self.schoolLogic.school

        if isinstance(asid, AssociationLogic):
            self.association_logic = asid
            self.assocation = asid.association
        elif isinstance(asid, Association):
            self.association_logic = AssociationLogic(self.auth, self.school, asid)
            self.assocation = asid
        else:
            self.association_logic = AssociationLogic(self.auth, self.school, asid)
            self.assocation = self.association_logic.association

        if isinstance(atid, AssociationAttendance):
            self.attendance = atid
        else:
            self.attendance = self.get_attendance(atid, is_version=is_version)

    def get_attendance(self, aid, is_version=False):
        """
        获取attendance
        :param aid:
        :param is_version:
        :return:
        """
        if is_version:
            attendance = AssociationAttendance.objects.filter(version=aid, association=self.assocation)
            if attendance.exists():
                return attendance[0]
        else:
            attendance = AssociationAttendance.objects.get_once(id=aid)
            if attendance is not None:
                return attendance

        raise AttendanceExcept.attendance_not_found()

    def check(self, *permission):
        """
        权限处理
        :param permission:
        :return:
        """
        if self.auth.get_account().role == int(RoleEnum.ADMIN):
            return True

        if not AttendanceLogic.inspect(self.auth.get_account(), self.assocation,
                                       self.attendance, self.association_logic.ass_acc, *permission):
            raise AssociationExcept.no_permission()

    @staticmethod
    def inspect(account, association, attendance, ass_acc=None, *permission):
        """
        权限判断
        :param account:
        :param association:
        :param attendance:
        :param ass_acc:
        :param permission:
        :return:
        """
        a_permission = json.loads(account.permissions)
        ass_permission = json.loads(association.configure)

        _att = ass_permission.get('attendance', dict())
        _end = attendance.end_time
        _start = attendance.start_time
        _manage = account.id in ass_permission.get('manage', [])

        if AssociationPermissionEnum.ATTENDANCE in permission:
            if association in account.association.all():
                if _start <= time.time() <= _end:
                    return True

        # 判断管理员权限
        if _manage or (ass_acc.role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]):
            return True

        # 检查考勤权限
        if _att is dict():
            return False

        if AssociationPermissionEnum.ATTENDANCE_VIEW in permission:
            if account.id in _att.get('views', list()):
                return True

        if AssociationPermissionEnum.ATTENDANCE_MANAGE in permission:
            if account.id in _att.get('manage', list()):
                return True

        return False

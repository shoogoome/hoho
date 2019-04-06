import random
import time

from common.entity.association.config import AssociationConfigureEntity
from common.entity.association.permissions import AssociationPermissionsEntity
from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.exceptions.association.info import AssociationExcept
from common.utils.helper.m_t_d import model_to_dict
from server.school.logic.info import SchoolLogic
from ..models import Association
from ..models import AssociationAccount, AssociationAttendance


class AssociationLogic(SchoolLogic):

    NORMAL_FIELDS = [
        'id', 'school', 'school__id', 'name', 'short_name', 'description'
    ]

    ADVANCED_FIELDS = [
        'backlog', 'config', 'colony', 'choosing_code'
    ]

    def __init__(self, auth, sid, aid=""):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        """
        super(AssociationLogic, self).__init__(auth, sid)
        self.account = None

        if isinstance(aid, Association):
            self.association = Association
        else:
            self.association = self.get_association(aid)
        # 自动检测是否在此协会
        if self.association is not None:
            self.account = self.get_association_account()

    def get_association(self, aid):
        """
        获取协会model
        :param aid:
        :return:
        """
        if aid == "" or aid is None:
            return None
        association = Association.objects.get_once(pk=aid)
        if association is None or association.school_id != self.school.id:
            raise AssociationExcept.association_not_found()
        return association

    def get_association_account(self):
        """
        获取人事表
        :return:
        """
        account = AssociationAccount.objects.filter_cache(
            account=self.auth.get_account(), association=self.association)
        if account is None or len(account) == 0:
            raise AssociationExcept.no_permission()
        return account

    def get_association_info(self):
        """
        获取协会信息
        :return:
        """
        # 普通用户
        field = self.NORMAL_FIELDS
        # 部长以上权限
        if self.inspect(AssociationPermissionEnum.ASSOCIATION_VIEW_DATA):
            field += self.ADVANCED_FIELDS
        return model_to_dict(self.association, field)

    def filter_account(self):
        """
        获取协会人事
        :return:
        """
        return AssociationAccount.objects.filter_cache(association=self.association)

    def get_config(self):
        """
        返回协会配置
        :return:
        """
        if self.association is None:
            return None
        return AssociationConfigureEntity.parse(self.association.config)

    @staticmethod
    def elective_code():
        """
        生成协会码
        :return:
        """
        code = ''
        for i in range(0, 8):
            code += str(random.randint(0, 9))
        return code

    def filter_attendance(self):
        """
        获取所有考勤记录
        :return:
        """
        return AssociationAttendance.objects.filter_cache(association=self.association)

    def check(self, *permission):
        """
        权限处理
        :param permission:
        :return:
        """
        # ！为了世界的和平 管理员权限在协会当中并不放行
        if not self.inspect(*permission):
            raise AssociationExcept.no_permission()

        return True

    def inspect(self, *permission, **kwargs):
        """
        权限检查
        :param permission:
        :return:
        """
        # 未加入该协会则没有任何权限
        if self.account is None:
            return False

        account = self.account
        # 会长拥有协会内最高权限
        if account.role == int(RoleEnum.PRESIDENT):
            return True
        # 检查协会管理权限
        if AssociationPermissionEnum.ASSOCIATION in permission:
            return False
        # 检查协会敏感数据查看权限
        elif AssociationPermissionEnum.ASSOCIATION_VIEW_DATA in permission:
            if account.role == int(RoleEnum.MINISTER):
                return True

        # 模块管理权限
        _permissions = AssociationPermissionsEntity.parse(account.permissions)
        permissions_dict = {
            AssociationPermissionEnum.ATTENDANCE: _permissions.attendance(),
            AssociationPermissionEnum.APPRAISING: _permissions.appraising(),
            AssociationPermissionEnum.INTERVIEW: _permissions.interview(),
            AssociationPermissionEnum.NOTICE: _permissions.notice(),
            AssociationPermissionEnum.REPOSITORY: _permissions.repository(),
            AssociationPermissionEnum.SCHEDULING: _permissions.scheduling(),
            AssociationPermissionEnum.TASK: _permissions.task(),
        }
        # 检查模块管理权限
        if permission in permissions_dict:
            for pm in permission:
                if permissions_dict[pm]:
                    return True
        elif AssociationPermissionEnum.DEPARTMENT in permission:
            department = kwargs.get('department', None)
            if department is not None:
                if department.manager.filter(id=account.id).exists():
                    return True
        # 检查考勤签到权限
        elif AssociationPermissionEnum.ATTENDANCE_SIGN in permission:
            attendance = kwargs.get('attendance', None)
            # 在考勤时间内放行
            if attendance is not None:
                if attendance.start_time < time.time() < attendance.end_time:
                    return True

        return False

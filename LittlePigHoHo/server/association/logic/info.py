import json
import re
import random

from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.exceptions.association.info import AssociationExcept
from server.school.logic.info import SchoolLogic
from server.school.models import School
from ..models import Association
from common.exceptions.scheduling.curriculum import CurriculumExcept
from common.entity.scheduling.curriculum import SchedulingCurriculumEntity
from server.school.logic.info import SchoolLogic
from ..models import AssociationAccount, AssociationAttendance
from common.entity.association.config import AssociationConfigureEntity
from common.utils.helper.m_t_d import model_to_dict

class AssociationLogic(SchoolLogic):

    ASS_NOMAL_FILE = [
        'id', 'association', 'school__id', 'school__name', 'name', 'short_name', 'logo', 'description',
    ]

    ASS_SECRECY_FILE = [
        'backlog', 'config', 'choosing_code',
    ]

    ADMIN_FILE = [
        'premium_level', 'premium_deadline', 'repository_size',
    ]

    def __init__(self, auth, sid, aid=""):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        """
        super(AssociationLogic, self).__init__(auth, sid)

        if isinstance(aid, Association):
            self.association = Association
        else:
            self.association = self.get_association(aid)
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
        ass_acc = AssociationAccount.objects.filter_cache(
            account=self.auth.get_account(), association=self.association)
        if ass_acc is not None and len(ass_acc) > 0:
            return ass_acc[0]
        return None

    def get_association_info(self):
        """
        获取协会信息
        :return:
        """
        # 获取全部信息或部分信息
        field = (self.ASS_SECRECY_FILE + self.ASS_NOMAL_FILE)
        #     if self.check(AssociationPermissionEnum.MANAGE) else self.ASS_NOMAL_FILE

        if self.auth.get_account().role == int(RoleEnum.ADMIN):
            field += self.ADMIN_FILE
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


    def get_curriculum(self):
        """
        获取无课表配置model
        :return:
        """
        curriculum = self.association.curriculum_set.all()

        if not curriculum.exists():
            raise CurriculumExcept.no_curriculum()
        return curriculum[0]
    
    def check_format(self, data):
        """
        检查无课表配置
        :param data: 
        :return: 
        """
        d_time = data.get('time', None)
        if d_time is None:
            return False
        time = SchedulingCurriculumEntity.parse(self.get_curriculum().content).dump().get('time')
        d_keys = d_time.keys()

        for key in d_keys:
            # 过滤time参数
            if len(re.findall('time', key)) <= 0:
                raise CurriculumExcept.format_error()

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

    # def check(self, *permission):
    #     """
    #     权限处理
    #     :param permission:
    #     :return:
    #     """
    #     if self.auth.get_account().role == int(RoleEnum.ADMIN):
    #         return True
    #     if not AssociationLogic.inspect(self.auth.get_account(), self.association, *permission):
    #         raise AssociationExcept.no_permission()
    #
    #     return True
    #
    # @staticmethod
    # def inspect(account, association, ass_acc=None, *permission):
    #     """
    #     权限检查
    #     :param account: 登陆account
    #     :param association: 协会model
    #     :param ass_acc: 协会人事表model
    #     :param permission: 判断权限
    #     :return:
    #     """
    #     account_permission = json.loads(account.permissions)
    #     ass_permission = json.loads(association.configure)
    #
    #     role = ass_acc.role if ass_acc is not None else None
    #     _att = ass_permission.get('attendance', dict())
    #     _manage = account.id in ass_permission.get('manage', [])
    #     # 查看协会权限（是否为协会成员）
    #     if AssociationPermissionEnum.VIEWS in permission:
    #         if ass_acc is not None:
    #             return True
    #     # 判断管理员权限
    #     if _manage or (role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]):
    #         return True
    #     # 添加协会成员权限 老师 会长 管理员 and 请求管理权限
    #     # if (AssociationPermissionEnum.MANAGE in permission) or (AssociationPermissionEnum.ADDDIRECTOR in permission):
    #     #     if role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]:
    #     #         return True
    #
    #     # 判断创建部门权限
    #     if AssociationPermissionEnum.DEPARTMENT_CREATE in permission:
    #         if role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]:
    #             return True
    #
    #     # 检查考勤权限
    #     if _att is dict():
    #         return False
    #
    #     if AssociationPermissionEnum.ATTENDANCE_CREATE in permission:
    #         if account.id in _att.get('create', list()):
    #             return True
    #
    #     return False

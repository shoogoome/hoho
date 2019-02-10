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


class AssociationLogic(object):

    def __init__(self, auth, sid, aid):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
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
        if isinstance(aid, Association):
            self.association = Association
        else:
            self.association = self.get_association(aid)
        self.ass_acc = self.get_association_account()

    def get_association(self, aid):
        """
        获取协会model
        :param aid:
        :return:
        """
        association = Association.objects.filter(id=aid, school=self.school)
        if association.exists():
            return association[0]
        raise AssociationExcept.association_not_found()

    def get_association_account(self):
        """
        获取人事表
        :return:
        """
        ass_acc = self.association.associationaccount_set.filter(account=self.auth.get_account())
        if ass_acc.exists():
            return ass_acc[0]
        return None

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
        return self.association.associationattendance_set.all()

    def check(self, *permission):
        """
        权限处理
        :param permission:
        :return:
        """
        if self.auth.get_account().role == int(RoleEnum.ADMIN):
            return True
        if not AssociationLogic.inspect(self.auth.get_account(), self.association, *permission):
            raise AssociationExcept.no_permission()

        return True

    @staticmethod
    def inspect(account, association, ass_acc=None, *permission):
        """
        权限检查
        :param account: 登陆account
        :param association: 协会model
        :param ass_acc: 协会人事表model
        :param permission: 判断权限
        :return:
        """
        account_permission = json.loads(account.permissions)
        ass_permission = json.loads(association.configure)

        role = ass_acc.role if ass_acc is not None else None
        _att = ass_permission.get('attendance', dict())
        _manage = account.id in ass_permission.get('manage', [])
        # 查看协会权限（是否为协会成员）
        if AssociationPermissionEnum.VIEWS in permission:
            if ass_acc is not None:
                return True
        # 判断管理员权限
        if _manage or (role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]):
            return True
        # 添加协会成员权限 老师 会长 管理员 and 请求管理权限
        # if (AssociationPermissionEnum.MANAGE in permission) or (AssociationPermissionEnum.ADDDIRECTOR in permission):
        #     if role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]:
        #         return True

        # 判断创建部门权限
        if AssociationPermissionEnum.DEPARTMENT_CREATE in permission:
            if role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]:
                return True

        # 检查考勤权限
        if _att is dict():
            return False

        if AssociationPermissionEnum.ATTENDANCE_CREATE in permission:
            if account.id in _att.get('create', list()):
                return True

        return False

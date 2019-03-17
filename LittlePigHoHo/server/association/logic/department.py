import json

from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.exceptions.association.department import DepartmentExcept
from server.school.logic.info import SchoolLogic
from server.school.models import School
from ..logic.info import AssociationLogic
from ..models import Association, AssociationDepartment


class DepartmentLogic(object):

    def __init__(self, auth, sid, aid, did):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        :param did:
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
        if isinstance(aid, AssociationLogic):
            self.associationLogic = aid
            self.association = aid.association
        elif isinstance(aid, Association):
            self.association = Association
            self.associationLogic = AssociationLogic(self.auth, sid, aid)
        else:
            self.associationLogic = AssociationLogic(self.auth, sid, aid)
            self.association = self.associationLogic.association
        if isinstance(did, AssociationDepartment):
            self.department = AssociationDepartment
        else:
            self.department = self.get_department(did)

    def get_department(self, did):
        """
        获取部门model
        :param did:
        :return:
        """
        departments = AssociationDepartment.objects.get_once(id=did)
        if departments is not None:
            return departments
        raise DepartmentExcept.department_not_found()

    def check(self, *permission):
        """
        权限处理
        :param permission:
        :return:
        """
        if self.auth.get_account().role == int(RoleEnum.ADMIN):
            return True

        if not DepartmentLogic.inspect(self.auth.get_account(), self.association,
                                       self.department, self.associationLogic.ass_acc, *permission):
            raise DepartmentExcept.no_permission()

    @staticmethod
    def inspect(account, association, department, ass_acc=None, *permission):
        """
        权限判断
        :param account:
        :param association:
        :param department:
        :param ass_acc:
        :param permission:
        :return:
        """
        dep_permission = json.loads(department.permissions)

        role = ass_acc.role if ass_acc is not None else None
        _manage = account.id in dep_permission.get('manage', [])

        if AssociationPermissionEnum.DEPARTMENT_VIEW in permission:
            if ass_acc is not None and ass_acc.department is department:
                return True

        # 判断删除部门权限
        if AssociationPermissionEnum.DEPARTMENT_DELETE in permission:
            if role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]:
                return True

        # 判断管理部门权限
        if AssociationPermissionEnum.DEPARTMENT_MANAGE in permission:
            if _manage or (role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]):
                return True

        return False

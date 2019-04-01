import json

from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.exceptions.association.department import DepartmentExcept
from ..logic.info import AssociationLogic
from ..models import AssociationDepartment
from common.utils.helper.m_t_d import model_to_dict


class DepartmentLogic(AssociationLogic):

    NOMAL_FILE = [
        'id', 'name', 'short_name', 'description', 'association',
        'association__id', 'association__name', 'manager',
        'manager__id', 'manager__nickname'
    ]

    def __init__(self, auth, sid, aid, did=""):
        """
        部门逻辑
        :param auth:
        :param sid:
        :param aid:
        :param did:
        """
        super(DepartmentLogic, self).__init__(auth, sid, aid)

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
        if did == "" or did is None:
            return None
        departments = AssociationDepartment.objects.get_once(pk=did)
        if departments is not None or departments.association_id != self.association.id:
            return departments
        raise DepartmentExcept.department_not_found()

    def get_department_info(self):
        """
        获取部门信息
        :return:
        """
        return model_to_dict(self.department, self.NOMAL_FILE)



    # def check(self, *permission):
    #     """
    #     权限处理
    #     :param permission:
    #     :return:
    #     """
    #     if self.auth.get_account().role == int(RoleEnum.ADMIN):
    #         return True
    #
    #     if not DepartmentLogic.inspect(self.auth.get_account(), self.association,
    #                                    self.department, self.associationLogic.ass_acc, *permission):
    #         raise DepartmentExcept.no_permission()

    # @staticmethod
    # def inspect(account, association, department, ass_acc=None, *permission):
    #     """
    #     权限判断
    #     :param account:
    #     :param association:
    #     :param department:
    #     :param ass_acc:
    #     :param permission:
    #     :return:
    #     """
    #     dep_permission = json.loads(department.permissions)
    #
    #     role = ass_acc.role if ass_acc is not None else None
    #     _manage = account.id in dep_permission.get('manage', [])
    #
    #     if AssociationPermissionEnum.DEPARTMENT_VIEW in permission:
    #         if ass_acc is not None and ass_acc.department is department:
    #             return True
    #
    #     # 判断删除部门权限
    #     if AssociationPermissionEnum.DEPARTMENT_DELETE in permission:
    #         if role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]:
    #             return True
    #
    #     # 判断管理部门权限
    #     if AssociationPermissionEnum.DEPARTMENT_MANAGE in permission:
    #         if _manage or (role in [int(RoleEnum.TEACHER), int(RoleEnum.PRESIDENT)]):
    #             return True
    #
    #     return False

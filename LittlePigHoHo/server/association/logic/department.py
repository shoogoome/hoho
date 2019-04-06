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
        if departments is None or departments.association_id != self.association.id:
            raise DepartmentExcept.department_not_found()
        return departments

    def get_department_info(self):
        """
        获取部门信息
        :return:
        """
        return model_to_dict(self.department, self.NOMAL_FILE)

    def check(self, permission):
        """
        权限处理
        :param permission:
        :return:
        """
        # ！为了世界的和平 管理员权限在协会当中并不放行
        if not self.inspect(permission, department=self.department):
            raise DepartmentExcept.no_permission()

        return True

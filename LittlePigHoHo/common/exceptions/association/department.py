
from common.exceptions.base import HoHoExceptBase

class DepartmentExcept(HoHoExceptBase):

    @classmethod
    def department_not_found(cls):
        return cls("查无此部门")

    @classmethod
    def no_permission(cls):
        return cls("无权限操作")

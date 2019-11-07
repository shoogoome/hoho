
from common.exceptions.base import HoHoExceptBase

class DepartmentExcept(HoHoExceptBase):

    @classmethod
    def department_not_found(cls):
        return cls("查无此部门")

    @classmethod
    def no_permission(cls):
        return cls("无权限操作")

    @classmethod
    def name_exist(cls):
        return cls("名称已存在")

    @classmethod
    def short_name_exist(cls):
        return cls("名称缩写已存在")

    @classmethod
    def no_affiliated_department(cls):
        return cls("没有归属部门")


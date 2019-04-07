
from common.exceptions.base import HoHoExceptBase

class AssociationExcept(HoHoExceptBase):

    @classmethod
    def association_not_found(cls):
        return cls("查无此协会")

    @classmethod
    def no_permission(cls):
        return cls("无权限操作")

    @classmethod
    def code_error(cls):
        return cls("协会码错误")

    @classmethod
    def not_account(cls):
        return cls("查无此账号")

    @classmethod
    def joined_association(cls):
        return cls("已加入该协会")

    @classmethod
    def department_not_exist(cls):
        return cls("该部门非协会内部部门")

    @classmethod
    def name_exists(cls):
        return cls("该名称已存在")

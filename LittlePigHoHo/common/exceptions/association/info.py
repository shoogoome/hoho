
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

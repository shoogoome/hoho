from common.exceptions.base import HoHoExceptBase

class SchoolInfoException(HoHoExceptBase):

    @classmethod
    def no_permission(cls):
        return cls("无权限执行此操作")

    @classmethod
    def create_error(cls):
        return cls("创建学校失败")

    @classmethod
    def school_not_found(cls):
        return cls("差无此学校")



from ..base import HoHoExceptBase

class InterviewInfoExcept(HoHoExceptBase):

    @classmethod
    def no_registration(cls):
        return cls("无该报名表")

    @classmethod
    def no_registration_template(cls):
        return cls("无该报名表模板")

    @classmethod
    def params_require(cls, par):
        return cls("参数{}必填".format(par))

    @classmethod
    def in_association(cls):
        return cls("已加入该协会")

    @classmethod
    def no_permission(cls):
        return cls("无权限执行此操作")

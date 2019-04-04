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

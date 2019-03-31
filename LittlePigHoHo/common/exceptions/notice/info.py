from ..base import HoHoExceptBase

class NoticeInfoExcept(HoHoExceptBase):

    @classmethod
    def no_notice(cls):
        return cls("无该报名表")




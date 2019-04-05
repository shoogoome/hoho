
from common.exceptions.base import HoHoExceptBase

class CurriculumExcept(HoHoExceptBase):

    @classmethod
    def format_error(cls):
        return cls("参数格式错误")

    @classmethod
    def no_curriculum(cls):
        return cls("无该无课表配置")




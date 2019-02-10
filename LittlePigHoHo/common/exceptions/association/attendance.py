from common.exceptions.base import HoHoExceptBase

class AttendanceExcept(HoHoExceptBase):

    @classmethod
    def attendance_not_found(cls):
        return cls("差无此考勤记录")

    @classmethod
    def time_out(cls):
        return cls("考勤已结束")
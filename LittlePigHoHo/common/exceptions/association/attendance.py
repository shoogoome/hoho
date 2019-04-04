from common.exceptions.base import HoHoExceptBase

class AttendanceExcept(HoHoExceptBase):

    @classmethod
    def attendance_not_found(cls):
        return cls("差无此考勤记录")

    @classmethod
    def time_out(cls):
        return cls("考勤已结束")

    @classmethod
    def title_exist(cls):
        return cls("标题以存在")

    @classmethod
    def no_in_place(cls):
        return cls("不在考勤地点范围之内")
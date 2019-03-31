from ..base import HoHoExceptBase

class TaskInfoExcept(HoHoExceptBase):

    @classmethod
    def no_task(cls):
        return cls("无此任务")

    @classmethod
    def no_task_report(cls):
        return cls("无此任务进度回报")



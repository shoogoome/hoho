from ..base import HoHoExceptBase

class TaskInfoExcept(HoHoExceptBase):

    @classmethod
    def no_task(cls):
        return cls("无此任务")

    @classmethod
    def no_task_report(cls):
        return cls("无此任务进度回报")

    @classmethod
    def no_working(cls):
        return cls("任务尚未接手执行")

    @classmethod
    def working(cls):
        return cls("任务已被领取或指派")

    @classmethod
    def no_permission(cls):
        return cls("无权限执行此操作")



from ..base import HoHoExceptBase

class AppraisingInfoExcept(HoHoExceptBase):

    @classmethod
    def score_template_no_exists(cls):
        return cls("评分模板不存在")

    @classmethod
    def score_no_100(cls):
        return cls("满分必须为100")

    @classmethod
    def score_no_exists(cls):
        return cls("评分表不存在")

    @classmethod
    def no_time_post(cls):
        return cls("已填写该对象评优")

    @classmethod
    def template_no_exists(cls):
        return cls("模版不存在")

    @classmethod
    def version_no_exists(cls):
        return cls("版本号不存在")

    @classmethod
    def config_error(cls):
        return cls("配置错误")


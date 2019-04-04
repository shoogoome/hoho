from ...core.dao.entityBase import EntityBase
from ...core.dao.proptype import PropType


class InterviewCustomEntity(EntityBase):

    def __init__(self, **kwargs):

        # 名称
        self.title = PropType.str(default="")

        # 是否必填
        self.require =  PropType.bool(default=False)

        # 默认值
        self.default = PropType.str(default="")

        # 解析参数
        super(InterviewCustomEntity, self).__init__(**kwargs)

from ...core.dao.entityBase import EntityBase
from ...core.dao.proptype import PropType


class InterviewRegistrationEntity(EntityBase):

    def __init__(self, **kwargs):

        # 专业
        self.major = PropType.str(default='')

        # 学院
        self.college = PropType.str(default='')

        # 电话
        self.phone = PropType.str(default='')

        # 自我介绍
        self.introduce = PropType.str(default='')

        # 自定义扩展字段
        self.custom_data = PropType.list(default='{}')

        # 解析参数
        super(InterviewRegistrationEntity, self).__init__(**kwargs)

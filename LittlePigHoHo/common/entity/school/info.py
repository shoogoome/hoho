from ...core.dao.entityBase import EntityBase
from ...core.dao.proptype import PropType


class SchoolEntity(EntityBase):

    def __init__(self, **kwargs):

        # 无课表配置
        self.curriculum = PropType.dict(default={})


        super(SchoolEntity, self).__init__(**kwargs)

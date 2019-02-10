from ...core.dao.entityBase import EntityBase
from ...core.dao.proptype import PropType


class SchedulingCurriculumEntity(EntityBase):

    def __init__(self, **kwargs):

        # 单天课程安排
        self.time = PropType.dict(default={}) # type: dict  {"time1": {"start_time": 0, "end_time": 0}}

        # 上课天数
        self.day = PropType.int(default=5)

        # 单天课程数量
        self.num = PropType.int(default=0)


        super(SchedulingCurriculumEntity, self).__init__(**kwargs)

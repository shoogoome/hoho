from ...core.dao.entityBase import EntityBase
from ...core.dao.proptype import PropType


class SchedulingCurriculumEntity(EntityBase):

    def __init__(self, **kwargs):

        # 单天课程安排
        self.time = PropType.dict(default={}) # type: dict  {"time1": {"start_time": "0", "end_time": "0"}}


        super(SchedulingCurriculumEntity, self).__init__(**kwargs)

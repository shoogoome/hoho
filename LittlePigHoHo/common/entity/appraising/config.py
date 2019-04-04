from common.core.dao.proptype import PropType
from common.core.dao.entityBase import EntityBase


class AppraisingConfigureEntity(EntityBase):

    def __init__(self, **kwargs):

        # 考勤占比
        self.attendance_proportion = PropType.float(default=0.3)

        # 请假等同旷会次数
        self.number_of_leave = PropType.int(default=2)

        # 版本号
        self.version = PropType.dict(default={})  # type: dict {"version": "template_id"}

        # 解析参数
        super(AppraisingConfigureEntity, self).__init__(**kwargs)
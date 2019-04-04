from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase
from ..appraising.config import AppraisingConfigureEntity

class AssociationConfigureEntity(EntityBase):

    def __init__(self, **kwargs):

        # 由于历史原因。。。。。命名惨不忍睹
        # 考勤占比
        self.attendance_proportion = PropType.float(default=0.3)

        # 请假等同旷会次数 （hoho1.0废弃）
        self.number_of_leave = PropType.int(default=2)

        # 版本号对应
        self.version_dict = PropType.dict(default={})    # type: dict {"version": {"template_id": id, "start_time": 0.0, "end_time": 0.0}}

        # 当前评优版本号
        self.version = PropType.int(default=0)

        # 当前面试版本号
        self.interview_version = PropType.int(default=0)

        # 面试版本号对应
        self.interview_version_dict = PropType.dict(default={})    # type: dict {"version": {"template_id": id, "start_time": 0.0, "end_time": 0.0}}

        # 解析参数
        super(AssociationConfigureEntity, self).__init__(**kwargs)
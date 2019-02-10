from ...core.dao.entityBase import EntityBase
from ...core.dao.proptype import PropType


class AssociationAttendanceEntity(EntityBase):

    def __init__(self, **kwargs):

        # 创建考勤权限
        self.create = PropType.list(default=[])
        # 查看考勤情况权限
        self.views = PropType.list(default=[])
        # 管理权限
        self.manage = PropType.list(default=[])


        # 解析参数
        super(AssociationAttendanceEntity, self).__init__(**kwargs)
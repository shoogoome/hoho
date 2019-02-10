from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase


class AssociationConfigureEntity(EntityBase):

    def __init__(self, **kwargs):

        # 临时管理员
        self.manage = PropType.list(default=[])
        # 考勤权限 继承attendanceEntity
        self.attendance = PropType.dict(default={})

        # 解析参数
        super(AssociationConfigureEntity, self).__init__(**kwargs)
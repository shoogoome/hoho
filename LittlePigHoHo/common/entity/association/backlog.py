from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase

class AssociationBacklog(EntityBase):

    def __init__(self, **kwargs):
        # 考勤情况
        self.attendance = PropType.dict(default={})

        super(AssociationBacklog, self).__init__(**kwargs)
from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase

class AssociationBacklog(EntityBase):

    def __init__(self, **kwargs):

        self.attendance = PropType.dict(default={})
from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase


class AssociationConfigureEntity(EntityBase):

    def __init__(self, **kwargs):
        # 评优配置

        # 解析参数
        super(AssociationConfigureEntity, self).__init__(**kwargs)
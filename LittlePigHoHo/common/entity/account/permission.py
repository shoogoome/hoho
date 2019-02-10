from ...core.dao.entityBase import EntityBase
from ...core.dao.proptype import PropType


class AccountPermissionEntity(EntityBase):

    def __init__(self, **kwargs):
        """
        INIT
        :param kwargs:
        """
        # 创建协会权限
        self.create = PropType.bool(default=False, required=True)
        # 可查看协会列表
        self.view = PropType.list(default=list(), required=True)

        # 解析参数
        super(AccountPermissionEntity, self).__init__(**kwargs)

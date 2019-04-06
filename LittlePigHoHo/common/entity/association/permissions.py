from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase


class AssociationPermissionsEntity(EntityBase):

    def __init__(self, **kwargs):
        """
        协会人事权限
        一方面用做模块负责人权限
        另外也可以用在储备部长权限调整
        :param kwargs:
        """
        # 绩效考核
        self.appraising = PropType.bool(default=False)

        # 面试模块
        self.interview = PropType.bool(default=False)

        # 通知模块
        self.notice = PropType.bool(default=False)

        # 资源仓库模块
        self.repository = PropType.bool(default=False)

        # 考勤模块
        self.attendance = PropType.bool(default=False)

        # 排班模块
        self.scheduling = PropType.bool(default=False)

        # 任务模块
        self.task = PropType.bool(default=False)

        # 解析参数
        super(AssociationPermissionsEntity, self).__init__(**kwargs)
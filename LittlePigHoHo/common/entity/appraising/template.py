from common.core.dao.proptype import PropType
from common.core.dao.entityBase import EntityBase


class AppraisingTemplateEntity(EntityBase):

    def __init__(self, **kwargs):

        # 题号
        self.number = PropType.int(default=1)

        # 题目描述
        self.title = PropType.str(default="")

        # 题目所占分数  满分100 所有题目所占分数必须等于100
        self.score = PropType.float(default=10.0)

        # 答案 格式：[A, B, C, D.....] n个答案 按数量比例划分分数 0号位0分  len-1号位满分
        self.answer = PropType.list(default=["A", "B"])

        # 解析参数
        super(AppraisingTemplateEntity, self).__init__(**kwargs)
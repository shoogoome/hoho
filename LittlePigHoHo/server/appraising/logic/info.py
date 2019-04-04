
from server.association.logic.info import AssociationLogic
from ..models import AppraisingScoreTemplate
from common.utils.helper.m_t_d import model_to_dict
from common.exceptions.appraising.info import AppraisingInfoExcept
from common.entity.appraising.template import AppraisingTemplateEntity

import json

class AppraisingLogic(AssociationLogic):

    FIELD = [
        'author', 'author__id', 'author__nickname', 'association', 'version',
        'association__id', 'title', 'config', 'create_time', 'update_time'
    ]

    def __init__(self, auth, sid, aid, pid=""):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        :param pid:
        """
        super(AppraisingLogic, self).__init__(auth, sid, aid)

        if isinstance(pid, AppraisingScoreTemplate):
            self.score_template = pid
        else:
            self.score_template = self.get_score_template(pid)

    def get_score_template(self, pid):
        """
        获取评分模版model
        :param pid:
        :return:
        """
        if pid == "" or pid is None:
            return
        score_template = AppraisingScoreTemplate.objects.get_once(pk=pid)
        if score_template is None or score_template.association_id != self.association.id:
            raise AppraisingInfoExcept.score_template_no_exists()

        return score_template

    def get_score_template_info(self):
        """
        获取评分模版信息
        :return:
        """
        if self.score_template is None:
            return
        return model_to_dict(self.score_template, self.FIELD)

    def get_template_config(self):
        """
        获取配置
        :return:
        """
        if self.score_template is None:
            return
        return json.loads(self.score_template.config)

    def config_format(self, config):
        """
        格式化配置
        :param config:
        :return:
        """
        problem = []
        # 检查满分是否为100分
        if sum([i.get('score', 0) for i in config]) != 100:
            raise AppraisingInfoExcept.score_no_100()
        # 构建config字段内容
        index = 1
        for cf in config:
            entity = AppraisingTemplateEntity()
            entity.update(cf)
            try:
                problem.append({
                    "number": index,
                    "title": entity.title(),
                    "score": entity.score(),
                    "answer": entity.answer()
                })
                index += 1
            except:
                pass
        return problem


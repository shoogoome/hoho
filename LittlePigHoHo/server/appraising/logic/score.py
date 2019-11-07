
from server.association.logic.info import AssociationLogic
from ..models import AppraisingScore, AppraisingScoreTemplate
from common.utils.helper.m_t_d import model_to_dict
from common.exceptions.appraising.info import AppraisingInfoExcept
from common.entity.appraising.template import AppraisingTemplateEntity
from common.core.dao.redis import RedisClusterFactory
from .redis import AppraisingRedis
import json


class AppraisingScoreLogic(AssociationLogic):

    FIELD = [
        'author', 'author__id', 'author__nickname', 'association', 'target', 'target__id',
        'target__nickname', 'association__id', 'template', 'template__id', 'content',
        'create_time', 'update_time', 'score'
    ]

    def __init__(self, auth, sid, aid, psid=""):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        :param pid:
        """
        super(AppraisingScoreLogic, self).__init__(auth, sid, aid)

        if isinstance(psid, AppraisingScore):
            self.score = psid
        else:
            self.score = self.get_score(psid)

        self._redis = None

    def get_score(self, psid):
        """
        获取评分模版model
        :param psid:
        :return:
        """
        if psid == "" or psid is None:
            return
        score = AppraisingScore.objects.get_once(pk=psid)
        if score is None or score.association_id != self.association.id:
            raise AppraisingInfoExcept.score_no_exists()

        return score

    def get_score_info(self):
        """
        获取评分模版信息
        :return:
        """
        if self.score is None:
            return
        return model_to_dict(self.score, self.FIELD)


    def get_version(self):
        """
        返回当前版本号
        :return:
        """
        return self.get_config().version()

    def get_template_id(self):
        """
        返回templateid
        :return:
        """
        version_config = self.get_config().version_dict()
        return version_config.get(str(self.get_version()), {}).get('template_id', -1)

    def get_redis(self):
        """
        返回redis
        :return:
        """
        if self._redis is None:
            self._redis = AppraisingRedis()
        return self._redis

    def content_to_score(self, content):
        """
        计算总分
        :param content:
        :return:
        """
        version = self.get_version()
        version_config = self.get_config().version_dict()
        # 过滤版本信息
        config = version_config.get(str(version), None)
        if config is None:
            raise AppraisingInfoExcept.config_error()
        # 检查模板
        template = AppraisingScoreTemplate.objects.get_once(pk=config.get('template_id'))
        if template is None:
            raise AppraisingInfoExcept.config_error()
        # 计算总分
        total_score = 0
        t_config = json.loads(template.config)
        for _config in t_config:
            length = len(_config.get('answer', []))
            try:
                total_score += _config.get('score', 0) * ((length - _config.get('answer', []).index(content.get(str(_config.get('number', 0)), -1))) / length)
            except:
                pass

        return float("{:.2f}".format(total_score))


from server.association.logic.info import AssociationLogic
from ..models import AssociationScheduling, AssociationCurriculum, AssociationAccountCurriculum
from common.exceptions.scheduling.curriculum import CurriculumExcept
from common.utils.helper.m_t_d import model_to_dict
from common.entity.scheduling.curriculum import SchedulingCurriculumEntity
import json

class CurriculumLogic(AssociationLogic):

    FIELD = [
        'title', 'association', 'association__id', 'content', 'update_time'
    ]

    ACCOUNT_FIELD = [
        'account', 'account__id', 'curriculum', 'curriculum__id',
        'content', 'update_time'
    ]


    def __init__(self, auth, sid, aid):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        """
        super(CurriculumLogic, self).__init__(auth, sid, aid)

        self.curriculum = self.get_curriculum()
        self.account_curriculum = None

    def get_curriculum(self):
        """
        获取无课表model
        :return:
        """
        return self.association.associationcurriculum_set.all()[0]

    def get_account_curriculum(self):
        """
        获取用户课表model
        :return:
        """
        if self.account_curriculum is None:
            account_curriculu = AssociationAccountCurriculum.objects.filter_cache(curriculum=self.curriculum, account=self.account)
            if len(account_curriculu) > 0:
                return account_curriculu[0]
        return None

    def get_account_curriculum_info(self):
        """
        获取用户课表信息
        :return:
        """
        if self.account_curriculum is None:
            self.account_curriculum = self.get_account_curriculum()
            if self.account_curriculum is None:
                return None
        return model_to_dict(self.account_curriculum, self.ACCOUNT_FIELD)


    def get_curriculum_info(self):
        """
        获取无课表信息
        :return:
        """
        if self.curriculum is None:
            return
        return model_to_dict(self.curriculum, self.FIELD)

    def get_association_curriculum_config(self):
        """
        获取协会课表配置
        :return:
        """
        if self.curriculum is None:
            return
        return SchedulingCurriculumEntity.parse(self.curriculum.content)



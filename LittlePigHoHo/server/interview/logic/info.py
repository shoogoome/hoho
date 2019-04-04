
from ..models import InterviewRegistrationTemplate
from server.school.models import School
from server.school.logic.info import SchoolLogic
from server.association.logic.info import AssociationLogic
from server.association.models import Association
from common.exceptions.interview.info import InterviewInfoExcept
from common.entity.interview.registration import InterviewRegistrationEntity
from common.entity.interview.custom import InterviewCustomEntity
from common.utils.helper.m_t_d import model_to_dict


class TemplateLogic(AssociationLogic):

    FIELD = [
        'association', 'association__id', 'author', 'author__id', 
        'config', 'update_time', 'title',
    ]

    def __init__(self, auth, sid, aid, rtid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        :param rtid:
        """
        super(TemplateLogic, self).__init__(auth, sid, aid)

        if isinstance(rtid, InterviewRegistrationTemplate):
            self.template = rtid
        else:
            self.template = self.get_template(rtid)

    def get_template(self, rtid):
        """
        获取报名表model
        :param rtid:
        :return:
        """
        if rtid == "" or rtid is None:
            return
        template = InterviewRegistrationTemplate.objects.get_once(pk=rtid)
        if template is None or template.association_id != self.association.id:
            raise InterviewInfoExcept.no_registration()
        return template

    def get_template_info(self):
        """
        获取报名表信息
        :return:
        """
        if self.template is None:
            return 
        return model_to_dict(self.template, self.FIELD)

    def config_format(self, config):
        """
        配置格式化
        :param config:
        :return:
        """
        template_entity = InterviewRegistrationEntity()
        template_entity.update(config)
        # 构建data
        data = {
            "major": template_entity.major(),
            "college": template_entity.college(),
            "phone": template_entity.phone(),
            "introduce": template_entity.introduce(),
            "custom_data": []
        }
        # 格式化自定义字段
        for custom in template_entity.custom_data():
            try:
                _entity = InterviewCustomEntity()
                _entity.update(custom)

                data['custom_data'].append({
                    "title": _entity.title(),
                    "require": _entity.require(),
                    "default": _entity.default()
                })
            except:
                pass
        return data









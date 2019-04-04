from common.entity.interview.registration import InterviewRegistrationEntity
from common.exceptions.interview.info import InterviewInfoExcept
from common.utils.helper.m_t_d import model_to_dict
from server.association.logic.info import AssociationLogic
from ..models import InterviewRegistration, InterviewRegistrationTemplate


class RegistrationLogic(AssociationLogic):
    FIELD = [
        'association', 'association__id', 'account', 'account__id',
        'content', 'update_time', 'version',
    ]

    def __init__(self, auth, sid, aid, rid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        :param rid:
        """
        super(RegistrationLogic, self).__init__(auth, sid, aid)

        if isinstance(rid, InterviewRegistration):
            self.registration = rid
        else:
            self.registration = self.get_registration(rid)

    def get_registration(self, rid):
        """
        获取报名表model
        :param rid:
        :return:
        """
        if rid == "" or rid is None:
            return
        registration = InterviewRegistration.objects.get_once(pk=rid)
        if registration is None or registration.association_id != self.association.id:
            raise InterviewInfoExcept.no_registration()
        return registration

    def get_registration_info(self):
        """
        获取报名表信息
        :return:
        """
        if self.registration is None:
            return
        return model_to_dict(self.registration, self.FIELD)

    def get_interview_version(self):
        """
        获取版本号
        :return:
        """
        config = super().get_config()
        return config.interview_version()

    def get_interview_config(self):
        """
        获取配置
        :return:
        """
        config = super().get_config()
        return config.interview_version_dict().get(config.interview_version(), {})

    def content_format(self, content):
        """
        格式化报名表
        :param content:
        :return:
        """
        # 获取当前版本对应模板id
        config = self.get_interview_config()
        tid = config.get(str(self.get_interview_version()), {}).get('template_id', -1)
        # 获取模板
        template = InterviewRegistrationTemplate.objects.get_once(pk=int(tid))
        if template is None:
            return InterviewInfoExcept.no_registration_template
            # 获取自定义字段配置
        _config = InterviewRegistrationEntity.parse(template.config)
        custom_data = _config.custom_data()
        # 格式化数据
        data = {
            'major': content.get('major', ""),
            'college': content.get('college', ""),
            'phone': content.get('phone', ""),
            'introduce': content.get('introduce', ""),
            'custom_data': {}
        }

        _custom_data = content.get('custom_data', {})
        for custom in custom_data:
            title = custom.get('title', "")
            info = _custom_data.get(title, None)
            # 不存在判断是否必填
            if info is None:
                if custom.get('require', True) is True:
                    raise InterviewInfoExcept.params_require(title)
                else:
                    data['custom_data'][title] = custom.get('default', "")
            else:
                data['custom_data'][title] = info
        return data
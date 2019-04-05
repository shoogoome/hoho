from ..models import School
from common.exceptions.school.info import SchoolInfoException
from common.exceptions.scheduling.curriculum import CurriculumExcept
from server.association.models import Association
from common.utils.helper.m_t_d import model_to_dict
from common.entity.school.info import SchoolEntity
from common.entity.scheduling.curriculum import SchedulingCurriculumEntity


class SchoolLogic(object):

    NORMAL_FIELDS = [
        'id', 'name', 'short_name', 'logo', 'description', 'config'
    ]


    def __init__(self, auth, sid, thown=True):
        """
        INIT
        :param sid:
        :param thown:
        """
        self.auth = auth
        if isinstance(sid, School):
            self.school = sid
        else:
            self.school = self.get_school(sid, thown)

    def get_school(self, sid, thown=True):
        """
        获取学校model
        :param sid:
        :param thown:
        :return:
        """
        schools = School.objects.get_once(pk=sid)
        if schools is None and thown:
            raise SchoolInfoException.school_not_found()
        return schools

    def get_school_config(self):
        """
        获取学校配置信息
        :return:
        """
        return SchoolEntity.parse(self.school.config)

    def get_school_info(self):
        """
        获取学习信息
        :return:
        """
        return model_to_dict(self.school, self.NORMAL_FIELDS)

    def filter_association(self):
        """
        获取协会列表
        :return:
        """
        return Association.objects.filter_cache(school=self.school)

    def get_school_curriculum_config(self):
        """
        获取学校无课表配置
        :return:
        """
        config = self.get_school_config()
        _config = SchedulingCurriculumEntity()
        _config.update(config.curriculum())
        return _config

    def curriculum_format(self, content):
        """
        格式化课表配置
        :return:
        """
        # 格式化配置
        data = {"time": {}}
        index = 1
        for _, v in content.items():
            data['time']["time{}".format(index)] = {
                "start_time": v.get('start_time', "0"),
                "end_time": v.get('end_time', "0")
            }
            index += 1

        return data
from ..models import School
from common.exceptions.school.info import SchoolInfoException
from common.exceptions.scheduling.curriculum import CurriculumExcept
from server.association.models import Association


class SchoolLogic(object):

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

    def filter_association(self):
        """
        获取协会列表
        :return:
        """
        return Association.objects.filter_cache(school=self.school)

    def get_curriculum(self):
        """
        获取无课表配置
        :return:
        """
        curriculum = self.school.curriculum_set.all()
        if not curriculum.exists():
            raise CurriculumExcept.no_curriculum()
        return curriculum[0]


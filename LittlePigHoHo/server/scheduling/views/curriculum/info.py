from common.core.http.view import HoHoView
from common.entity.scheduling.curriculum import SchedulingCurriculumEntity
from common.exceptions.scheduling.curriculum import CurriculumExcept
from common.utils.helper.params import ParamsParser
from server.school.logic.info import SchoolLogic
from server.scheduling.models import Curriculum
from common.utils.helper.result import Result
from common.utils.helper.m_t_d import model_to_dict
from common.core.auth.check_login import check_login
from server.association.logic.info import AssociationLogic


class CurriculumInfo(HoHoView):

    FILES = ['title', 'association', 'school__id', 'school__name',
             'school__short_name', 'description', 'content']

    @check_login
    def post(self, request, sid, aid):
        """
        配置无课表
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = AssociationLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)

        time = params.dict('time', desc='单天课程安排')
        day = params.int('day', desc='一周上课天数', require=False, default=5)

        b = [x for i in list(time.values()) for x in i.keys()]
        if set(b) != {'start_time', 'end_time'}:
            raise CurriculumExcept.format_error()

        curriculum = Curriculum.objects.create(
            title="%s无课表" % logic.school.name,
            association=logic.association,
            description="%s无课表",
            content=SchedulingCurriculumEntity(time=time, day=day, num=len(time)).dumps()
        )

        return Result(id=aid)

    @check_login
    def get(self, request, sid, aid):
        """
        查询协会无课表配置
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = AssociationLogic(self.auth, sid, aid)
        # 权限
        return Result(model_to_dict(logic.get_curriculum(), self.FILES))

    @check_login
    def put(self, request, sid, aid):
        """
        修改无课表配置
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = AssociationLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        curriculum = logic.get_curriculum()

        content = {}
        if params.has('time'):
            time = params.dict('time', desc='单天课程安排')
            # 判断格式
            b = {x for i in list(time.values()) for x in i.keys()}
            if b != {'start_time', 'end_time'}:
                raise CurriculumExcept.format_error()
            content['time'] = time
            content['num'] = len(time)

        if params.has('day'):
            day = params.int('day', desc='一周上课天数')

            content['day'] = day
        curriculum_content = SchedulingCurriculumEntity.parse(curriculum.content)
        curriculum_content.update(content)

        with params.diff(curriculum):
            curriculum.title = params.str('title', desc='标题')
            curriculum.description = params.str('description', desc='描述')
        curriculum.save()

        return Result(id=aid)

    @check_login
    def delete(self, request, sid, aid):
        """
        删除组织无课表配置
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = AssociationLogic(self.auth, sid, aid)
        # 权限判断
        curriculum = logic.get_curriculum()
        curriculum.delete()

        return Result(id=aid)



# class CurriculumAccount(HoHoView):
#
#     # data true 有课
#     # 无课表 true 无课
#
#     def fet:
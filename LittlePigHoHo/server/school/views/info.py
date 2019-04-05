import json

from django.http import *
from common.core.http.view import HoHoView

from common.core.auth.check_login import check_login
from common.enum.account.role import RoleEnum
from common.utils.helper.m_t_d import model_to_dict
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.account.logic.info import AccountLogic
from ..logic.info import SchoolLogic
from common.exceptions.school.info import SchoolInfoException
from ..models import School
from common.utils.helper.pagination import slicer
from django.db.models import Q

class SchoolView(HoHoView):

    def get(self, request, sid):
        """
        获取学校信息
        :param request:
        :param sid:
        :return:
        """
        logic = SchoolLogic(self.auth, sid)
        return Result(data=logic.get_school_info(), association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid=''):
        """
        创建学校
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.JSON)

        school = School.objects.create(
            name=params.str('name', desc='学校名称'),
            short_name=params.str('short_name', desc='缩写', require=False, default=''),
            description=params.str('description', desc='简介', require=False, default=''),
        )

        return Result(id=school.id, association_id=self.auth.get_association_id())

    @check_login
    def put(self, request, sid):
        """
        修改学校信息
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = SchoolLogic(self.auth, sid)

        school = logic.school
        if params.has('config'):
            config = params.dict('config', desc='配置')
            school.config = json.dumps({
                "curriculum": logic.curriculum_format(config)
            })
        with params.diff(school):
            school.name = params.str('name', desc='学校名称')
            school.short_name = params.str('short_name', desc='缩写')
            school.description = params.str('description', desc='简介')

            school.save()

        return Result(id=school.id, association_id=self.auth.get_association_id())

    @check_login
    def delete(self, request, sid):
        """
        删除学校
        :param request:
        :param sid:
        :return:
        """
        # if self.auth.get_account().role != int(RoleEnum.ADMIN):
        #     raise SchoolInfoException.no_permission()

        logic = SchoolLogic(self.auth, sid, True)
        logic.school.delete()

        return Result(id=sid, association_id=self.auth.get_association_id())


class SchoolList(HoHoView):


    def get(self, request):
        """
        获取学校列表
        :return:
        """
        params = ParamsParser(request.GET)

        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        schools = School.objects.values(
            'id', 'update_time').all()

        if params.has('key'):
            key = params.str('key', desc='关键字 名称 缩写')
            schools = schools.filter(
                Q(name__contains=key) |
                Q(short_name__contains=key)
            )

        @slicer(
            schools,
            limit=limit,
            page=page
        )
        def get_school_list(obj):
            return obj

        schools, pagination = get_school_list()
        return Result(schools=schools, pagination=pagination, association_id=self.auth.get_association_id())

    def post(self, request):
        """
        批量获取学校信息
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        ids = params.list('ids', desc='id列表')

        data = []
        schools = School.objects.get_many(ids=ids)
        for school in schools:
            try:
                logic = SchoolLogic(self.auth, school)
                data.append(logic.get_school_info())
            except:
                pass
        return Result(data=data, association_id=self.auth.get_association_id())




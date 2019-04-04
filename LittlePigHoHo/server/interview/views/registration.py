from django.db.models import Q

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.registra import RegistrationLogic
from ..models import InterviewRegistration
import json


class RegistrationInfo(HoHoView):

    @check_login
    def post(self, request, sid, aid):
        """
        填写报名表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        content = params.dict('content', desc='正文信息')

        registra = InterviewRegistration.objects.create(
            association=logic.association,
            version=logic.get_interview_version(),
            account=self.auth.get_account(),
            content=json.dumps(logic.content_format(content)),
        )

        return Result(id=registra.id, association_id=self.auth.get_association_id())

    @check_login
    def get(self, request, sid, aid, rid):
        """
        获取报名表信息
        :param request:
        :param sid:
        :param aid:
        :param rid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid, rid)

        return Result(data=logic.get_registration_info(), association_id=self.auth.get_association_id())

    @check_login
    def delete(self, request, sid, aid, rid):
        """
        删除报名表
        :param request:
        :param sid:
        :param aid:
        :param rid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid, rid)
        logic.registration.delete()

        return Result(id=rid, association_id=self.auth.get_association_id())


class RegistrationView(HoHoView):

    def get(self, request, sid, aid):
        """
        获取报名表列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid)
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        registrations = InterviewRegistration.objects.values('id', 'update_time').filter(association=logic.association)

        if params.has('version'):
            registrations = registrations.filter(version=params.int('version', desc='版本号'))
        if params.has('key'):
            key = params.str('key', desc='关键字 报名用户昵称 真实名称')
            registrations = registrations.filter(
                Q(account__nickname__contains=key) |
                Q(account__realname__contains=key)
            )

        registrations, pagination = slicer(registrations, limit=limit, page=page)()()
        return Result(registrations=registrations, pagination=pagination, association_id=self.auth.get_association_id())

    def post(self, request, sid, aid):
        """
        批量获取报名表信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='id列表')

        registrations = InterviewRegistration.objects.get_many(ids=ids)
        data = []
        for registration in registrations:
            try:
                logic.registration = registration
                data.append(logic.get_registration_info())
            except:
                pass
        return Result(data=data, association_id=self.auth.get_association_id())
         
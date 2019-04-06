import json

from django.db.models import Q

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.info import TemplateLogic
from common.enum.association.permission import AssociationPermissionEnum
from ..models import *


class RegistrationTemplateInfo(HoHoView):

    @check_login
    def post(self, request, sid, aid):
        """
        创建报名表模板
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = TemplateLogic(self.auth, sid, aid)
        # logic.check(AssociationPermissionEnum.INTERVIEW)

        params = ParamsParser(request.JSON)

        title = params.str('title', desc='标题')
        config = params.list('config', desc='配置正文')

        template = InterviewRegistrationTemplate.objects.create(
            association=logic.association,
            title=title,
            author=logic.account,
            config=json.dumps(logic.config_format(config)),
        )

        return Result(id=template.id, association_id=self.auth.get_association_id())

    @check_login
    def get(self, request, sid, aid, rtid):
        """
        获取报名表模板信息
        :param request:
        :param sid:
        :param aid:
        :param rtid:
        :return:
        """
        logic = TemplateLogic(self.auth, sid, aid, rtid)

        return Result(data=logic.get_template_info(), association_id=self.auth.get_association_id())

    @check_login
    def put(self, request, sid, aid, rtid):
        """
        修改面试模板信息
        :param request:
        :param sid:
        :param aid:
        :param rtid:
        :return:
        """
        logic = TemplateLogic(self.auth, sid, aid, rtid)
        # logic.check(AssociationPermissionEnum.INTERVIEW)
        params = ParamsParser(request.JSON)
        template = logic.template

        if params.has('title'):
            template.title = params.str('title', desc='标题')
        if params.has('config'):
            template.config = json.dumps(logic.config_format(params.list('config', desc='配置信息')))

        template.save()
        return Result(id=rtid, association_id=self.auth.get_association_id())

    @check_login
    def delete(self, request, sid, aid, rtid):
        """
        删除报名表模板
        :param request:
        :param sid:
        :param aid:
        :param rtid:
        :return:
        """
        logic = TemplateLogic(self.auth, sid, aid, rtid)
        # logic.check(AssociationPermissionEnum.INTERVIEW)
        logic.template.delete()

        return Result(id=rtid, association_id=self.auth.get_association_id())


class RegistrationTemplateView(HoHoView):

    @check_login
    def get(self, request, sid, aid):
        """
        获取报名表模板列表
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = TemplateLogic(self.auth, sid, aid)
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        templates = InterviewRegistrationTemplate.objects.values('id', 'update_time').filter(
            association=logic.association)

        if params.has('key'):
            key = params.str('key', desc='关键字 标题 创建人昵称')
            templates = templates.filter(
                Q(title__contains=key) |
                Q(author__nickname__contains=key)
            )

        templates, pagination = slicer(templates, limit=limit, page=page)()()

        return Result(templates=templates, pagination=pagination, association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        批量获取报名表模板信息
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = TemplateLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='id列表')

        templates = InterviewRegistrationTemplate.objects.get_many(ids=ids)
        data = []
        for template in templates:
            try:
                logic.template = template
                data.append(logic.get_template_info())
            except:
                pass
        return Result(data=data, association_id=self.auth.get_association_id())
           
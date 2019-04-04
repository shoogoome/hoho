import json

from common.core.http.view import HoHoView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.info import AppraisingLogic
from ..models import AppraisingScoreTemplate
from common.utils.helper.pagination import slicer


class AppraisingView(HoHoView):

    def get(self, request, sid, aid, pid):
        """
        获取评分模版信息
        :param request:
        :param sid:
        :param aid:
        :param pid:
        :return:
        """
        logic = AppraisingLogic(self.auth, sid, aid, pid)

        return Result(data=logic.get_score_template_info(), association_id=self.auth.get_association_id())

    def post(self, request, sid, aid):
        """
        创建评分模版
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AppraisingLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        title = params.str('title', desc='标题')
        config = params.list('config', desc='配置（题目配置）')

        problem = logic.config_format(config)

        template = AppraisingScoreTemplate.objects.create(
            author=logic.account,
            association=logic.association,
            title=title,
            config=json.dumps(problem)
        )

        return Result(id=template.id, association_id=self.auth.get_association_id())

    def put(self, request, sid, aid, pid):
        """
        修改评分模版信息
        :param request:
        :param sid:
        :param aid:
        :param pid:
        :return:
        """
        logic = AppraisingLogic(self.auth, sid, aid, pid)
        params = ParamsParser(request.JSON)
        template = logic.score_template

        if params.has('config'):
            config = params.list('config', desc='配置（题目配置）')
            template.config = json.dumps(logic.config_format(config))

        with params.diff(template):
            template.title = params.str('title', desc='标题')

        template.save()
        return Result(id=pid, association_id=self.auth.get_association_id())

    def delete(self, request, sid, aid, pid):
        """
        删除评分模版
        :param request:
        :param sid:
        :param aid:
        :param pid:
        :return:
        """
        logic = AppraisingLogic(self.auth, sid, aid, pid)

        logic.score_template.delete()
        return Result(id=pid, association_id=self.auth.get_association_id())



class AppraisingInfo(HoHoView):

    def get(self, request, sid, aid):
        """
        获取评分表列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AppraisingLogic(self.auth, sid, aid)
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        template = AppraisingScoreTemplate.objects.values('id', 'update_time').filter(association=logic.association)

        if params.has('title'):
            template = template.filter(title__contains=params.str('title', desc='标题'))

        templates, pagination = slicer(template, limit=limit, page=page)()()
        return Result(templates=templates, pagination=pagination, association_id=self.auth.get_association_id())


    def post(self, request, sid , aid):
        """
        批量获取评分表信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AppraisingLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)

        ids = params.list('ids', desc='id列表')
        templates = AppraisingScoreTemplate.objects.get_many(ids=ids)

        data = []
        for template in templates:
            try:
                logic.score_template = template
                data.append(logic.get_score_template_info())
            except:
                pass
        return Result(data=data, association_id=self.auth.get_association_id())




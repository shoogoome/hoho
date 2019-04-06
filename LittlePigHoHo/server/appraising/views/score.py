import json

from common.core.http.view import HoHoView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.score import AppraisingScoreLogic
from ..logic.info import AppraisingLogic
from ..models import AppraisingScoreTemplate, AppraisingScore
from common.utils.helper.pagination import slicer
from server.association.models import AssociationAccount
from common.exceptions.association.info import AssociationExcept
from common.exceptions.appraising.info import AppraisingInfoExcept
from django.db.models import Q
from common.core.auth.check_login import check_login
from common.enum.association.permission import AssociationPermissionEnum


class AppraisingScoreView(HoHoView):


    @check_login
    def get(self, request, sid, aid, psid):
        """
        获取评分表信息
        :param request:
        :param sid:
        :param aid:
        :param psid:
        :return:
        """
        logic = AppraisingScoreLogic(self.auth, sid, aid, psid)
        # logic.check(AssociationPermissionEnum.APPRAISING, AssociationPermissionEnum.ASSOCIATION_VIEW_DATA)

        return Result(data=logic.get_score_info(), association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        提交评分表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AppraisingScoreLogic(self.auth, sid, aid)
        # logic.check(AssociationPermissionEnum.APPRAISING, AssociationPermissionEnum.ASSOCIATION_VIEW_DATA)

        params = ParamsParser(request.JSON)
        target_id = params.int('target_id', desc='填写对象id')
        content = params.dict('content', desc='评分正文')           # type: dict {"number": "answer"}
        # 检查目标用户是否符合标准
        if not AssociationAccount.objects.filter(association=logic.association, id=target_id).exists():
            raise AssociationExcept.not_account()
        # 过滤非发起评优时段提交 或 已填写过
        if AppraisingScore.objects.filter(target_id=target_id, association=logic.association).exists():
            raise AppraisingInfoExcept.no_time_post()

        score = AppraisingScore.objects.create(
            author=logic.account,
            association=logic.association,
            target_id=target_id,
            content=json.dumps(content),
            version=logic.get_version(),
            score=logic.content_to_score(content),
            template_id=logic.get_template_id(),
        )

        return Result(id=score.id, association_id=self.auth.get_association_id())

    @check_login
    def put(self, request, sid, aid, psid):
        """
        修改评分表
        :param request:
        :param sid:
        :param aid:
        :param psid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = AppraisingScoreLogic(self.auth, sid, aid, psid)
        # if logic.score.author_id != logic.account.id:
        #     raise AssociationExcept.no_permission()

        score = logic.score

        if params.has('content'):
            content = params.dict('content', desc='评分正文')
            score.content = json.dumps(content)
            score.score = logic.content_to_score(content)
        score.save()

        return Result(id=psid, association_id=self.auth.get_association_id())

    @check_login
    def delete(self, request, sid, aid, psid):
        """
        删除评分表
        :param request:
        :param sid:
        :param aid:
        :param psid:
        :return:
        """
        logic = AppraisingScoreLogic(self.auth, sid, aid, psid)
        # if logic.score.author_id != logic.account.id:
        #     logic.check(AssociationPermissionEnum.APPRAISING)

        logic.score.delete()
        return Result(id=psid, association_id=self.auth.get_association_id())



class AppraisingScoreInfo(HoHoView):

    @check_login
    def get(self, request, sid, aid):
        """
        获取评分列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AppraisingScoreLogic(self.auth, sid, aid)
        # logic.check(AssociationPermissionEnum.APPRAISING)

        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        score = AppraisingScore.objects.values('id', 'update_time').filter(association=logic.association)

        if params.has('author'):
            score = score.filter(author_id=params.int('author', desc='提交人id'))

        if params.has('version'):
            score = score.filter(version=params.int('version', desc='版本号'))

        if params.has('target'):
            score = score.filter(target_id=params.int('target', desc='被评价人id'))

        if params.has('key'):
            key = params.str('key', desc='关键字 提交者昵称 对象昵称')
            score = score.filter(
                Q(author__nickname__contains=key) |
                Q(target__nickname__contains=key)
            )

        scores, pagination = slicer(score, limit=limit, page=page)()()

        return Result(scores=scores, pagination=pagination, association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        批量获取评分信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = AppraisingScoreLogic(self.auth, sid, aid)
        # logic.check(AssociationPermissionEnum.APPRAISING)

        ids = params.list('ids', desc='id列表')
        scores = AppraisingScore.objects.get_many(ids=ids)

        data = []
        for score in scores:
            try:
                logic.score = score
                data.append(logic.get_score_info())
            except:
                pass

        return Result(data=data, association_id=self.auth.get_association_id())





import json

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ...logic.curriculum import CurriculumLogic
from ...models import AssociationAccountCurriculum
from ...logic.redis import SchedulingRedis
from server.association.models import AssociationAccount
import json


class CurriculumInfo(HoHoView):
    RESET = False

    @check_login
    def get(self, request, sid, aid):
        """
        查询协会无课表配置  或 重置无课表信息
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = CurriculumLogic(self.auth, sid, aid)
        if self.RESET:
            logic.curriculum.content = logic.get_school_curriculum_config().dumps()
            logic.curriculum.save()
            return Result(association_id=self.auth.get_association_id())
        # 权限
        return Result(data=logic.get_curriculum_info(), association_id=self.auth.get_association_id())

    @check_login
    def put(self, request, sid, aid):
        """
        修改无课表配置
        :param request: 
        :param sid: 
        :param aid: 
        :return: 
        """
        logic = CurriculumLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        curriculum = logic.curriculum

        if params.has('title'):
            curriculum.title = params.str('title', desc='标题')
        if params.has('content'):
            content = params.dict('content', desc='内容')
            data = logic.curriculum_format(content)
            curriculum.content = json.dumps(data)

        curriculum.save()
        return Result(association_id=self.auth.get_association_id())

class CurriculumView(HoHoView):

    SUMMARY = False

    def post(self, request, sid, aid):
        """
        填写课表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = CurriculumLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        content = params.list('content', desc='课表内容')
        _config = logic.get_association_curriculum_config()
        keys = _config.time().keys()
        # 格式化课表
        data = {"day{}".format(i): {k: False for k in keys} for i in range(1, 8)}
        index = 1
        for _time in content:
            try:
                data["day{}".format(index)].update({k: v for k, v in _time.items()})
                index += 1
            except:
                pass

        curriculum = AssociationAccountCurriculum.objects.filter_cache(curriculum=logic.curriculum, account=logic.account)
        # 修改
        if len(curriculum) > 0:
            curriculum = curriculum[0]
            curriculum.content = json.dumps(data)
            curriculum.save()
        # 创建
        else:
            curriculum = AssociationAccountCurriculum.objects.create(
                account=logic.account,
                curriculum=logic.curriculum,
                content=json.dumps(data),
            )

        return Result(id=curriculum.id, association_id=self.auth.get_association_id())


    def get(self, request, sid, aid):
        """
        汇总无课表 or 获取课表信息
        :param request:
        :param sid:
        :param aid:
        :return:  redis key scheduling:协会id:
        """

        redis = SchedulingRedis()
        logic = CurriculumLogic(self.auth, sid, aid)
        # 获取课表信息
        if not self.SUMMARY:
            return Result(data=logic.get_account_curriculum_info(), association_id=self.auth.get_association_id())

        # 汇总无课表  不包括退休人员
        _id = str(logic.association.id)
        if redis.exists(_id):
            data = json.loads(redis.get(_id).decode())
        else:
            curriculums = AssociationAccountCurriculum.objects.filter_cache(curriculum=logic.curriculum, account__retire=False)
            account_ids = AssociationAccount.objects.values('id').filter(association=logic.association, retire=False)
            config = logic.get_association_curriculum_config()
            keys = config.time().keys()

            data = {"day{}".format(i): {k:[] for k in keys} for i in range(1, 8)}
            # 构建无课表
            for curriculum in curriculums:
                # 获取该账户信息
                content = json.loads(curriculum.content)
                nickname = curriculum.account.nickname
                # 填充账户无课表信息
                for index, _time in content.items():
                    for k, v in _time.items():
                        if not v:
                            data[index][k].append(nickname)

            data['completion'] = account_ids.count() / len(curriculums)
            redis.set(_id, json.dumps(data))

        return Result(data=data, association_id=self.auth.get_association_id())

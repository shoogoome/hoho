import time
import json

from common.core.auth.check_login import check_login
from common.core.dao.redis import get_redis_conn
from common.core.http.view import HoHoView
from common.enum.association.permission import AssociationPermissionEnum
from common.utils.helper.m_t_d import model_to_dict
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..models import *
from common.entity.interview.registration import InterviewRegistrationEntity
from server.association.logic.info import AssociationLogic
from ..logic.info import RegistrationLogic
from common.exceptions.association.attendance import AttendanceExcept
from common.entity.association.backlog import AssociationBacklog
from common.exceptions.interview.info import InterviewInfoExcept


class RegistrationTemplateInfo(HoHoView):

    FIELD = [
        'title', 'version', 'additional', 'start_time', 'end_time', 'using'
    ]

    ENTITY = [
        'major', 'college', 'phone', 'introduce', 'additional'
    ]

    @check_login
    def post(self,request, sid, aid):
        """
        创建报名表模板
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid, aid)

        # 延用历史版本
        # 权限
        params = ParamsParser(request.JSON)
        version = -1
        # 历史版本可沿用历史版本信息但时间需重新设置
        if params.has('version'):
            version = params.float('version', desc='版本号')
            registration_terplate = RegistrationTemplate.objects.filter(
                association=logic.association, version=version)
            if not registration_terplate.exists():
                raise InterviewInfoExcept.no_registration_template()
            registration_terplate = registration_terplate[0]
        title = params.str('title', desc='标题') if version == -1 else registration_terplate.title
        major = params.str('major', desc='专业') if version == -1 else ''
        college = params.str('college', desc='学院') if version == -1 else ''
        phone = params.str('phone', desc='电话') if version == -1 else ''
        introduce = params.str('introduce', desc='自我介绍') if version == -1 else ''
        additional = params.dict('additional', desc='附加信息', default={}, require=False)

        # additional 信息过滤检查 附加信息黑名单过滤
        if version == -1:
            ad_entity = InterviewRegistrationEntity(
                major=major, college=college, phone=phone, introduce=introduce, **additional)

        registration = RegistrationTemplate.objects.create(
            association=logic.association,
            title=title,
            additional=ad_entity.dumps() if version == -1 else registration_terplate.additional,
            using=False
        )

        return Result(id=registration.id)

    @check_login
    def get(self, request, sid, aid, rid):
        """
        获取面试模板信息
        :param request:
        :param sid:
        :param aid:
        :param rid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid, rid, model=True)

        return Result(data=model_to_dict(logic.registration_template, fields=self.FIELD))

    @check_login
    def put(self, request, sid, aid, rid):
        """
        修改面试模板信息
        :param request:
        :param sid:
        :param aid:
        :param rid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid, rid, model=True)
        params = ParamsParser(request.JSON)
        registration_template = logic.registration_template

        with params.diff(registration_template):
            registration_template.title = params.str('title', desc='标题')

        additional_eneity = InterviewRegistrationEntity.parse(registration_template.additional)
        for entity in self.ENTITY:
            if params.has(entity):
                if entity == 'additional':
                    additional_eneity.update(**params.dict(entity))
                else:
                    additional_eneity.update(params.str(entity))

        registration_template.additional = additional_eneity.dumps()
        registration_template.save()

        return Result(id=rid)

    @check_login
    def delete(self, request, sid, aid, rid):
        """
        删除报名表模板
        :param request:
        :param sid:
        :param aid:
        :param rid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid, rid, model=True)
        logic.registration_template.delete()

        return Result(id=rid)


class RegistrationTemplateManage(HoHoView):

    USE = True

    @check_login
    def get(self, request, sid, aid, rid):
        """
        启用面试模板 or 不启用模板
        :param request:
        :param sid:
        :param aid:
        :param rid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid, rid)
        if self.USE:
            logic.using_template()
        else:
            logic.nouse_template()

        return Result(id=rid)




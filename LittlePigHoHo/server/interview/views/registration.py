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
        template = logic.get_using_template()

        realname = params.str('realname', desc='姓名')
        major = params.str('major', desc='专业')
        college = params.str('college', desc='学院')
        phone = params.str('phone', desc='联系方式')
        introduce = params.str('introduce', desc='自我介绍')
        additional = params.dict('additional', desc='附加信息', require=False, default={})

        _additional = InterviewRegistrationEntity.parse(template.additional)













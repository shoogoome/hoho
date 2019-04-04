from common.core.http.view import HoHoView
from common.entity.association.config import AssociationConfigureEntity
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.models import AssociationAccount
from ..logic.registra import RegistrationLogic
from ..models import InterviewRegistration


class InterviewManage(HoHoView):
    FILTER = True

    def get(self, request, sid, aid):
        """
        发起招新
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid)
        params = ParamsParser(request.GET)
        template_id = params.int('template_id', desc='使用模板id')
        start_time = params.float('start_time', desc='开始时间')
        end_time = params.float('end_time', desc='结束时间')
        # 更新协会配置
        config = AssociationConfigureEntity.parse(logic.association.config)
        interview_version_dict = config.interview_version_dict()

        interview_version_dict[str(config.interview_version() + 1)] = {
            "template_id": template_id,
            "start_time": start_time,
            "end_time": end_time
        }
        config.interview_version = logic.get_interview_version() + 1
        config.interview_version_dict = interview_version_dict

        logic.association.config = config.dumps()
        logic.association.save()

        return Result(association_id=self.auth.get_association_id(), status="success")

    def post(self, request, sid, aid):
        """
        过滤报名表 or 导入协会
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = RegistrationLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        version = logic.get_interview_version()
        status = {}

        # 过滤报名表
        if self.FILTER:
            status = {}
            ids = params.list('ids', desc='过滤报名表id')
            registrations = InterviewRegistration.objects.get_many(ids=ids)
            for registration in registrations:
                if registration.association_id == logic.association.id:
                    status[str(registration.id)] = 1
                    registration.delete()
                else:
                    status[str(registration.id)] = 0
        # 导入协会
        else:
            registrations = InterviewRegistration.objects.filter_cache(association=logic.association, version=version)

            # 创建人事表
            for registration in registrations:
                try:
                    AssociationAccount.objects.create(
                        association=logic.association,
                        nickname=registration.account.realname,
                        account=registration.account
                    )
                    _status = 1
                except:
                    _status = 0
                status[str(registration.id)] = _status

        return Result(status=status, association_id=self.auth.get_association_id())

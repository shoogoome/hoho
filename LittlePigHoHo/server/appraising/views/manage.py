from common.core.http.view import HoHoView
from common.enum.account.role import RoleEnum
from common.exceptions.appraising.info import AppraisingInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.logic.attendance import AttendanceLogic
from server.association.models import AssociationAccount
from ..logic.score import AppraisingScoreLogic
from ..models import AppraisingScoreTemplate, AppraisingScore


class AppraisingManageView(HoHoView):

    def get(self, request, sid, aid):
        """
        发起评优
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AppraisingScoreLogic(self.auth, sid, aid)
        params = ParamsParser(request.GET)
        template_id = params.int('template_id', desc='模板id')

        if not AppraisingScoreTemplate.objects.filter(id=template_id, association=logic.association).exists():
            raise AppraisingInfoExcept.template_no_exists()

        # 更新版本号及版本关联
        config = logic.get_config()
        version_dict = config.version_dict()
        version_dict[str(logic.get_version() + 1)] = {
            "template_id": template_id,
            "start_time": params.float('start_time', desc='开始时间'),
            "end_time": params.float('end_time', desc='结束时间')
        }
        config.version = config.version() + 1
        config.version_dict = version_dict
        logic.association.config = config.dumps()
        logic.association.save()

        return Result(association_id=self.auth.get_association_id(), status="success")

    def post(self, request, sid, aid):
        """
        总结评优
        :param request:
        :param sid:
        :param aid:
        :return:   redis key   appraising:协会id:version
        """
        logic = AppraisingScoreLogic(self.auth, sid, aid)
        atlogic = AttendanceLogic(self.auth, sid, aid)
        params = ParamsParser(request.JSON)
        version = params.int('version', desc='版本号')

        redis = logic.get_redis()
        name = "{}:{}".format(logic.association.id, version)
        # 获取缓存数据
        if redis.exists(name):
            data = {k.decode(): float(v.decode()) for k, v in redis.hgetall(name).items()}
        else:
            config = logic.get_config()
            version_config = config.version_dict().get(str(version), None)
            # 检验版本号
            if version_config is None:
                raise AppraisingInfoExcept.version_no_exists()
            # 获取协会所有在职干事账户
            accounts = AssociationAccount.objects.values('id').filter(association=logic.association, retire=False,
                                                                      role=int(RoleEnum.DIRECTOR))
            # 获取提交的所干事评优表
            scores = AppraisingScore.objects.filter_cache(association=logic.association, version=version)
            # 获取评优数据
            start_time = version_config.get('start_time', 0.0)
            end_time = version_config.get('end_time', 0.0)
            attendance_proportion = config.attendance_proportion()
            # 获取考勤情况
            _status = atlogic.get_range_sign_info(start_time, end_time)
            total = _status["total"]

            data = {}
            for score in scores:
                _id = str(score.target_id)
                status = _status[_id]
                # 考勤分数
                score_att = attendance_proportion * ((status[0] + status[1]) / total) * 100

                # 总分
                data[str(score.target.nickname)] = float(
                    "{:.2f}".format(score_att + ((1 - attendance_proportion) * score.score)))
            # 进度

            data['completion'] = len(scores) / accounts.count()
            # 数据缓存 时间一周
            redis.hmset(name, data)

        return Result(data=data, association_id=self.auth.get_association_id())

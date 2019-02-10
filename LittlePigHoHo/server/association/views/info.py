import json

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.enum.account.permission import AccountPermissionEnum
from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.exceptions.association.info import AssociationExcept
from common.utils.helper.m_t_d import model_to_dict
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.account.logic.info import AccountLogic
from server.school.logic.info import SchoolLogic
from ..logic.info import AssociationLogic
from ..models import Association, AssociationAccount
from common.entity.association.config import AssociationConfigureEntity
from common.entity.association.attendance import AssociationAttendanceEntity
from common.entity.account.permission import AccountPermissionEntity
from common.entity.association.backlog import AssociationBacklog

class AssociationInfoView(HoHoView):
    NOMAL_FILE = [
        'id', 'name'
    ]

    ASS_NOMAL_FILE = [
        'id', 'association', 'school__id', 'school__name', 'name', 'short_name', 'logo', 'description',
    ]

    ASS_SECRECY_FILE = [
        'backlog', 'config', 'choosing_code', 'master_administrator'
    ]

    ADMIN_FILE = [
        'premium_level', 'premium_deadline', 'repository_size',
    ]

    def get(self, request, sid, aid=''):
        """
        获取协会列表 or 获取协会信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        if aid != '':
            alogic = AssociationLogic(self.auth, sid, aid)
            field = (self.ASS_SECRECY_FILE + self.ASS_NOMAL_FILE) \
                if alogic.check(AssociationPermissionEnum.MANAGE) else self.ASS_NOMAL_FILE
            if self.auth.get_account().role == int(RoleEnum.ADMIN):
                field += self.ADMIN_FILE
            return Result(model_to_dict(alogic.association, field))

        slogic = SchoolLogic(self.auth, sid)
        data = [model_to_dict(_ass, self.NOMAL_FILE) for _ass in slogic.school.association_set.all()]
        return Result(data)

    @check_login
    def post(self, request, sid):
        """
        创建协会
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.JSON)
        alogic = AccountLogic(self.auth, thown=False)
        alogic.check(AccountPermissionEnum.CREATE_ASSOCIATION)
        slogic = SchoolLogic(self.auth, sid)

        att_config = AssociationAttendanceEntity().dump()
        config = AssociationConfigureEntity()
        config.set_value('attendance', att_config)
        associatime = Association.objects.create(
            name=params.str('name', desc='名称'),
            short_name=params.str('short_name', desc='缩写', require=False, default=''),
            description=params.str('description', desc='简介', require=False, default=''),
            choosing_code=AssociationLogic.elective_code(),
            config=config.dumps(),
            backlog=AssociationBacklog().dumps(),
            school=slogic.school,
            # logo=upload(request.FILES.get('image', None), SCHOOL_LOGO),
        )
        associatime.save()

        AssociationAccount.objects.create(
            account=self.auth.get_account(),
            association=associatime,
            role=int(RoleEnum.PRESIDENT)
        )

        if self.auth.get_account().role != int(RoleEnum.ADMIN):
            account = self.auth.get_account()
            permissions = AccountPermissionEntity.parse(account.permissions)
            permissions.set_value('create', False)
            account.permissions = permissions.dumps()
            account.save()

        return Result(id=associatime.id)

    @check_login
    def put(self, request, sid, aid):
        """
        修改协会信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        alogic = AssociationLogic(self.auth, sid, aid)
        alogic.check(AssociationPermissionEnum.MANAGE)
        association = alogic.association

        with params.diff(association):
            association.name = params.str('name', desc='名称')
            association.short_name = params.str('short_name', desc='缩写')
            association.description = params.str('description', desc='简介')
            # logo=upload(request.FILES.get('image', None), SCHOOL_LOGO),
            association.save()

        return Result(id=association.id)

    @check_login
    def delete(self, request, sid, aid):
        """
        删除协会
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        if self.auth.get_account().role != int(RoleEnum.ADMIN):
            raise AssociationExcept.no_permission()

        alogic = AssociationLogic(self.auth, sid, aid)
        alogic.association.delete()

        return Result(id=aid)


class AssociationVerification(HoHoView):
    APPLY = False

    @check_login
    def get(self, request, sid, aid):
        """
        重置协会码 or 新人加入协会
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid, aid)
        # 加入协会
        if self.APPLY:
            params = ParamsParser(request.GET)
            choosing_code = params.str('choosing_code')
            if logic.association.choosing_code != choosing_code:
                raise AssociationExcept.code_error()

            ata = AssociationAccount.objects.create(
                association=logic.association,
                account=self.auth.get_account(),
            )
            return Result(id=ata.id)

        # 重置协会码
        logic.check(AssociationPermissionEnum.MANAGE)

        logic.association.choosing_code = AssociationLogic.elective_code()
        logic.association.save()

        return Result(id=logic.association.id)

    @check_login
    def put(self, request, sid, aid):
        """
        修改用户权限（协会）
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        alogic = AssociationLogic(self.auth, sid, aid)
        alogic.check(AssociationPermissionEnum.MANAGE)

        association = alogic.association
        params = ParamsParser(request.JSON)
        data = params.dict('data', desc='数据')

        """
        data = {
            "account": {
                "id": int(权限)
            },
            "attendance": {
                "views": [],
                "create": [],
                "manage": [],
            }
        }
        """

        result = []
        ass_acc = association.associationaccount_set.all()

        # 更新用户信息
        if alogic.ass_acc.role in [int(RoleEnum.TEACHER),
                                   int(RoleEnum.PRESIDENT)]:
            for _aid in data.get('account', {}):
                _s_c = ass_acc.filter(account_id=int(_aid))
                if _s_c.exists():
                    if alogic.ass_acc.role == int(RoleEnum.PRESIDENT) and \
                            data['account'].get(_aid, 0) == int(RoleEnum.TEACHER):
                        continue
                    if data['account'][_aid] in [int(RoleEnum.DIRECTOR),
                                                 int(RoleEnum.MINISTER),
                                                 int(RoleEnum.PRESIDENT),
                                                 int(RoleEnum.TEACHER)]:
                        _s_c[0].role = int(data['account'][_aid])
                        _s_c[0].save()

        a_permission = json.loads(association.configure)

        _att = data.get('attendance', {})
        for per in ['views', 'create', 'manage']:
            if _att.get(per, None) is None:
                continue
            a_permission[per] = _att.get(per)
        association.configure = json.dumps(a_permission)
        association.save()

        return Result(status=result)

    # @check_login
    # def post(self, request, sid, aid):
    #     """
    #     处理申请（加入协会申请）
    #     :param request:
    #     :param sid:
    #     :param aid:
    #     :return:
    #     """
    #     params = ParamsParser(request.JSON)
    #
    #     logic = AssociationLogic(self.auth, sid, aid)
    #     logic.check(AssociationPermissionEnum.ADDDIRECTOR)
    #
    #     backlog = json.loads(logic.association.backlog)
    #     handle = params.dict('handle', desc='处理情况') # {aid: states}
    #
    #     status = {}
    #     for a_id, _stu in handle.items():
    #         # 处理待办事项
    #         if backlog['apple'].get(a_id, None) is None:
    #             status[a_id] = 0
    #             continue
    #         del backlog['apply'][a_id]
    #
    #         # 处理用户
    #         alogic = AccountLogic(self.auth, int(a_id), thown=False)
    #         if alogic.account is None:
    #             status[a_id] = 0
    #             continue
    #         a_permission = json.loads(alogic.account.permissions)
    #         if a_permission['views'].get(a_id, None) is None:
    #             status[a_id] = 0
    #             continue
    #         if _stu not in [int(AccountStatesEnum.PENDING),
    #                                     int(AccountStatesEnum.SUCCESS),
    #                                     int(AccountStatesEnum.FAIL)]:
    #             status[a_id] = 0
    #             continue
    #         a_permission['views'][a_id] = _stu
    #         alogic.account.permission = json.dumps(a_permission)
    #         alogic.account.save()
    #         status[a_id] = 1
    #         continue
    #
    #     logic.association.backlog = json.dumps(backlog)
    #     logic.association.save()
    #
    #     return Result(status=status)


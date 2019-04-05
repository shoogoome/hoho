from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
# from common.entity.association.attendance import AssociationAttendanceEntity
from common.entity.account.permission import AccountPermissionEntity
from common.entity.association.config import AssociationConfigureEntity
from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.utils.helper.m_t_d import model_to_dict
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.school.logic.info import SchoolLogic
from ..logic.info import AssociationLogic
from ..models import Association
from ..models import AssociationAccount
from django.db.models import Q
from common.utils.helper.pagination import slicer
from server.scheduling.models import AssociationCurriculum
import json

class AssociationInfoView(HoHoView):

    VERSION = False

    def get(self, request, sid, aid):
        """
        获取协会列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid, aid)

        # 获取评优版本信息
        if self.VERSION:
            return Result(data=logic.get_config().version_dict, association_id=self.auth.get_association_id())
        return Result(logic.get_association_info(), association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid):
        """
        创建协会
        :param request:
        :param sid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid)
        params = ParamsParser(request.JSON)
        account = self.auth.get_account()

        # 权限检查 暂不进行
        # alogic = AccountLogic(self.auth, thown=False)
        # alogic.check(AccountPermissionEnum.CREATE_ASSOCIATION)
        slogic = SchoolLogic(self.auth, sid)

        # 创建协会
        config = AssociationConfigureEntity()
        association = Association.objects.create(
            name=params.str('name', desc='名称'),
            short_name=params.str('short_name', desc='缩写', require=False, default=''),
            description=params.str('description', desc='简介', require=False, default=''),
            choosing_code=AssociationLogic.elective_code(),
            config=config.dumps(),
            school=slogic.school,
            # logo=upload(request.FILES.get('image', None), SCHOOL_LOGO),
        )

        # 创建课表配置
        AssociationCurriculum.objects.create(
            title="{}课表配置".format(association.name),
            association=association,
            content=logic.get_school_curriculum_config().dumps()
        )

        # 创建协会人事关联
        AssociationAccount.objects.create(
            nickname=account.realname,
            account=account,
            association=association,
            role=int(RoleEnum.PRESIDENT),
        )

        # 非系统管理员只拥有一次性创建协会权限
        if self.auth.get_account().role != int(RoleEnum.ADMIN):
            account = self.auth.get_account()
            permissions = AccountPermissionEntity.parse(account.permissions)
            permissions.create = False
            account.permissions = permissions.dumps()
            account.save()

        return Result(id=association.id, association_id=self.auth.get_association_id())

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
        # alogic.check(AssociationPermissionEnum.MANAGE)
        association = alogic.association

        with params.diff(association):
            association.name = params.str('name', desc='名称')
            association.short_name = params.str('short_name', desc='缩写')
            association.description = params.str('description', desc='简介')
            # logo=upload(request.FILES.get('image', None), SCHOOL_LOGO),
            association.save()

        return Result(id=association.id, association_id=self.auth.get_association_id())

    @check_login
    def delete(self, request, sid, aid):
        """
        删除协会
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        # if self.auth.get_account().role != int(RoleEnum.ADMIN):
        #     raise AssociationExcept.no_permission()

        alogic = AssociationLogic(self.auth, sid, aid)
        alogic.association.delete()

        return Result(id=aid, association_id=self.auth.get_association_id())


class AssociationVerification(HoHoView):

    LIST = False

    @check_login
    def get(self, request, sid, aid=""):
        """
        重置协会码 or 获取协会列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        # 重置协会码
        if not self.LIST:
            logic = AssociationLogic(self.auth, sid, aid)
            # logic.check(AssociationPermissionEnum.MANAGE)

            logic.association.choosing_code = AssociationLogic.elective_code()
            logic.association.save()
            return Result(id=aid)
        # 获取协会列表
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)
        associations = Association.objects.values('id', 'update_time').filter(school__id=sid)

        if params.has('key'):
            key = params.str('key', desc='关键字 名称 缩写')
            associations = associations.filter(
                Q(name__contains=key) |
                Q(short_name__contains=key)
            )

        @slicer(
            associations,
            limit=limit,
            page=page
        )
        def get_associations_list(obj):
            return obj

        associations, pagination = get_associations_list()
        return Result(associations=associations, pagination=pagination, association_id=self.auth.get_association_id())

    def post(self, request, sid):
        """
        批量获取协会信息
        :param request:
        :param sid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid)
        params = ParamsParser(request.JSON)

        ids = params.list('ids', desc='协会id')
        associations = Association.objects.get_many(ids=ids)

        data = []
        for association in associations:
            try:
                logic.association = association
                data.append(logic.get_association_info())
            except:
                pass

        return Result(data=data, association_id=self.auth.get_association_id())










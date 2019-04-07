from django.db.models import Q

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.decorate.administrators import administrators
from common.entity.account.permission import AccountPermissionEntity
from common.entity.association.config import AssociationConfigureEntity
from common.enum.account.role import RoleEnum
from common.enum.association.permission import AssociationPermissionEnum
from common.exceptions.association.info import AssociationExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.scheduling.models import AssociationCurriculum
from ..logic.info import AssociationLogic
from ..models import Association
from ..models import AssociationAccount


class AssociationInfoView(HoHoView):
    VERSION = False

    def get(self, request, sid, aid):
        """
        获取协会列表 or 获取评优版本信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid, aid)

        # 获取评优版本信息
        if self.VERSION:
            check_login(lambda x: True)(self)
            # 敏感数据权限 部长以上即放行
            # logic.check(AssociationPermissionEnum.ASSOCIATION_VIEW_DATA)
            return Result(data=logic.get_config().version_dict, association_id=self.auth.get_association_id())
        return Result(data=logic.get_association_info(), association_id=self.auth.get_association_id())

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

        # 权限检查
        # permission_entity = AccountPermissionEntity.parse(self.auth.get_account().permissions)
        # if not permission_entity.create():
        #     raise AssociationExcept.no_permission()

        # 创建协会
        name = params.str('name', desc='名称')
        if Association.objects.values('id').filter(school__id=sid, name=name).exists():
            raise AssociationExcept.name_exists()

        config = AssociationConfigureEntity()
        association = Association.objects.create(
            name=name,
            short_name=params.str('short_name', desc='缩写', require=False, default=''),
            description=params.str('description', desc='简介', require=False, default=''),
            choosing_code=AssociationLogic.elective_code(),
            config=config.dumps(),
            school=logic.school,
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
        # alogic.check(AssociationPermissionEnum.ASSOCIATION)
        association = alogic.association

        with params.diff(association):
            association.name = params.str('name', desc='名称')
            association.short_name = params.str('short_name', desc='缩写')
            association.description = params.str('description', desc='简介')
            association.save()

        return Result(id=association.id, association_id=self.auth.get_association_id())

    @check_login
    # @administrators
    def delete(self, request, sid, aid):
        """
        删除协会  仅系统管理员有权限删除协会
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        alogic = AssociationLogic(self.auth, sid, aid)
        alogic.association.delete()

        return Result(id=aid, association_id=self.auth.get_association_id())


class AssociationVerification(HoHoView):
    LIST = False

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
            check_login(lambda x: True)(self)
            logic = AssociationLogic(self.auth, sid, aid)
            # logic.check(AssociationPermissionEnum.ASSOCIATION_VIEW_DATA)

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
            try:
                key = int(key)
                associations = associations.filter(
                    Q(name__contains=key) |
                    Q(short_name__contains=key) |
                    Q(id=key)
                )
            except:
                associations = associations.filter(
                    Q(name__contains=key) |
                    Q(short_name__contains=key)
                )

        associations, pagination = slicer(associations, limit=limit, page=page)()()
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
                logic.account = logic.get_association_account()
                data.append(logic.get_association_info())
            except:
                pass

        return Result(data=data, association_id=self.auth.get_association_id())

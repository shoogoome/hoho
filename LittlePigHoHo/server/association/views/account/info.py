from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.entity.association.permissions import AssociationPermissionsEntity
from common.enum.account.role import RoleEnum
from common.exceptions.association.info import AssociationExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.logic.account import AssociationAccountLogic
from server.association.logic.info import AssociationLogic
from server.association.models import AssociationAccount
from common.enum.association.permission import AssociationPermissionEnum
from ...models import AssociationDepartment


class AssociationAccountInfo(HoHoView):

    ME = False

    @check_login
    def get(self, request, sid, aid, acid=""):
        """
        获取用户信息(协会) or 自己
        :param request:
        :param sid:
        :param aid:
        :param acid:
        :return:
        """
        if self.ME:
            logic = AssociationAccountLogic(self.auth, sid, aid)
            logic.other_account = logic.account
        else:
            logic = AssociationAccountLogic(self.auth, sid, aid, acid)
        return Result(data=logic.get_account_info(), association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        加入协会
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        logic = AssociationLogic(self.auth, sid)
        logic.association = logic.get_association(aid)
        account = self.auth.get_account()

        params = ParamsParser(request.JSON)
        choosing_code = params.str('choosing_code')
        if logic.association.choosing_code != choosing_code:
            _status = -1
        else:
            # 判断是否已加入该协会
            _account = AssociationAccount.objects.filter(
                association=logic.association,
                account=account,
            )
            if _account.exists():
                _status = 1
            else:
                ata = AssociationAccount.objects.create(
                    nickname=account.nickname,
                    association=logic.association,
                    account=account,
                )
                _status = 0

        return Result(status=_status, association_id=self.auth.get_association_id())

    @check_login
    def put(self, request, sid, aid, acid=""):
        """
        修改用户信息
        :param request:
        :param sid:
        :param aid:
        :param acid:
        :return:
        """
        params = ParamsParser(request.JSON)
        alogic = AssociationAccountLogic(self.auth, sid, aid, acid)

        if acid != "":
            # alogic.check(AssociationPermissionEnum.ASSOCIATION)
            account = alogic.other_account
            # 角色修改
            if params.has('role'):
                # 缺少权限判断 输入过滤
                role = params.int('role', desc='用户角色')
                # 若是部长 则需添加部门id信息
                if role == int(RoleEnum.MINISTER):
                    department_id = params.int('department_id', desc='部门id')
                    department = AssociationDepartment.objects.get_once(pk=department_id)
                    # 过滤部门不存在或非该协会部门
                    if department is None or department.association_id != account.association_id:
                        raise AssociationExcept.department_not_exist()
                    # 更新数据库信息
                    account.department_id = department_id
                    department.manager.add(account)
                    department.save()
                # 若此前是部长但现在不是则清除部门部长信息
                elif account.role == int(RoleEnum.MINISTER):
                    # 查询quertset对象 因为反正都会被修改所以没必要使用filter_cache 性能反而不如filter
                    department = AssociationDepartment.objects.filter(
                        association_id=aid, manager__id=account.id)
                    # 去除管理员关联（部长）
                    if department.exists():
                        department = department[0]
                        department.manager.remove(account)
                        department.save()
                    account.department = None
                account.role = role
            # 权限修改
            if params.has('permissions'):
                permissions = AssociationPermissionsEntity.parse(account.permissions)
                permissions.update(params.dict('permissions', desc='权限'))
                account.permissions = permissions.dumps()
            # 部门修改
            if params.has('department'):
                # 过滤为本协会部门
                department = AssociationDepartment.objects.get_once(pk=params.int('department', desc='部门id'))
                if department is not None and department.association_id == alogic.association.id:
                    account.department = department
            # 退休换届
            if params.has('retire'):
                account.retire = params.bool('retire', desc='退休换届与否')
        else:
            account = alogic.account

        with params.diff(account):
            account.nickname = params.str('nickname', desc='协会内昵称')

        account.save()
        return Result(id=acid, association_id=self.auth.get_association_id())

    @check_login
    def delete(self, request, sid, aid, acid=""):
        """
        移出协会 or 退出协会
        :param request:
        :param sid:
        :param aid:
        :param acid:
        :return:
        """
        alogic = AssociationAccountLogic(self.auth, sid, aid, acid)

        if acid != "":
            # alogic.check(AssociationPermissionEnum.ASSOCIATION)
            account = alogic.other_account
        else:
            account = alogic.account

        account.delete()

        return Result(id=acid, association_id=self.auth.get_association_id())


class AssociationAccountView(HoHoView):

    @check_login
    def get(self, request, sid, aid):
        """
        获取协会用户列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        # 自动权限检查
        logic = AssociationLogic(self.auth, sid, aid)
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        accounts = AssociationAccount.objects.values('id', 'update_time').filter(association__id=aid)

        if params.has('key'):
            accounts = accounts.filter(nickname__contains=params.str('key', desc='关键字'))
        if params.has('role'):
            accounts = accounts.filter(role=params.int('role', desc='身份'))
        if params.has('retire'):
            accounts = accounts.filter(retire=params.bool('retire', desc='退休与否'))
        if params.has('department'):
            accounts = accounts.filter(department__id=params.int('department', desc='部门id'))

        accounts, pagination = slicer(accounts, limit=limit, page=page)()()
        return Result(accounts=accounts, pagination=pagination, association_id=self.auth.get_association_id())

    @check_login
    def post(self, request, sid, aid):
        """
        批量获取协会用户信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = AssociationAccountLogic(self.auth, sid, aid)

        ids = params.list('ids', desc='用户id列表')

        data = []
        accounts = AssociationAccount.objects.filter_cache(association__id=aid, id__in=ids)
        for account in accounts:
            try:
                logic.other_account = account
                data.append(logic.get_account_info())
            except:
                pass

        return Result(data=data, association_id=self.auth.get_association_id())

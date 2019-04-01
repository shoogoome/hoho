import json

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.enum.association.permission import AssociationPermissionEnum

from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from server.association.logic.department import DepartmentLogic
from server.association.logic.info import AssociationLogic
from server.association.models import AssociationDepartment
from common.exceptions.association.department import DepartmentExcept
from ...models import AssociationAccount
from django.db.models import Q
from common.utils.helper.pagination import slicer


class DepartmentInfo(HoHoView):


    @check_login
    def get(self, request, sid, aid, did):
        """
        获取部门信息
        :param request:
        :param sid:
        :param aid:
        :param did:
        :return:
        """
        logic = DepartmentLogic(self.auth, sid, aid, did)

        return Result(data=logic.get_department_info())

    @check_login
    def post(self, request, sid, aid):
        """
        创建部门
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = AssociationLogic(self.auth, sid, aid)

        name = params.str('name', desc='部门名称')
        short_name = params.str('short_name', desc='缩写')

        # 过滤参数
        departments = AssociationDepartment.objects.filter(association=logic.association)
        if departments.filter(name=name).exists():
            raise DepartmentExcept.name_exist()

        if departments.filter(short_name=short_name).exists():
            raise DepartmentExcept.short_name_exist()

        departmenr = AssociationDepartment.objects.create(
            name=name,
            short_name=short_name,
            description=params.str('description', desc="描述", require=False, default=""),
            association=logic.association
        )

        return Result(id=departmenr.id)

    @check_login
    def put(self, request, sid, aid, did):
        """
        修改部门信息
        :param request:
        :param sid:
        :param aid:
        :param did:
        :return:
        """
        # 添加删除管理员 还没做
        params = ParamsParser(request.JSON)
        logic = DepartmentLogic(self.auth, sid, aid, did)

        department = logic.department

        name = params.str('name', desc='部门名称')
        short_name = params.str('short_name', desc='缩写')

        # 过滤参数
        departments = AssociationDepartment.objects.filter(association=logic.association).exclude(id=did)
        if params.has('name'):
            if departments.filter(name=name).exists():
                raise DepartmentExcept.name_exist()
            department.name = name

        if params.has('short_name'):
            if departments.filter(short_name=short_name).exists():
                raise DepartmentExcept.short_name_exist()
            department.short_name = short_name

        if params.has('config'):
            config = params.dict('config', desc='配置信息')
            department.config = json.dumps(config)

        with params.diff(department):
            department.description = params.str('description', desc='简介')

        department.save()

        return Result(id=did)

    @check_login
    def delete(self, request, sid, aid, did):
        """
        删除部门
        :param request:
        :param sid:
        :param aid:
        :param did:
        :return:
        """
        dlogic = DepartmentLogic(self.auth, sid, aid, did)
        dlogic.department.delete()

        return Result(id=did)

class DepartmentView(HoHoView):

    def get(self, request, sid, aid):
        """
        获取协会部门列表
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        department = AssociationDepartment.objects.values('id', 'update_time').filter(association__id=aid)
        if params.has('key'):
            key = params.str('key', desc='关键字 名称 缩写')
            department = department.filter(
                Q(name__contains=key) |
                Q(short_name__contains=key)
            )

        @slicer(department, limit=limit, page=page)
        def get_department_list(obj):
            return obj

        departments, pagination = get_department_list()

        return Result(departments=departments, pagination=pagination)


    def post(self, request, sid, aid):
        """
        批量获取协会部门信息
        :param request:
        :param sid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = DepartmentLogic(self.auth, sid, aid)

        ids = params.list('ids', desc='部门id列表')

        data = []
        departments = AssociationDepartment.objects.get_many(ids=ids)
        for department in departments:
            logic.department = department
            try:
                data.append(logic.get_department_info())
            except:
                pass

        return Result(data)


class DepartmentMatters(HoHoView):

    @check_login
    def post(self, request, sid, aid, did):
        """
        批量添加用户到指定部门
        :param request:
        :param sid:
        :param aid:
        :param did:
        :return: {id: status 0-成功 1-非协会成员 2-已加入其他部门 3-未知原因失败}
        """
        logic = DepartmentLogic(self.auth, sid, aid, did)

        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='用户id')

        status = {}
        accounts = AssociationAccount.objects.get_many(ids=ids)
        for account in accounts:
            try:
                # 过滤非同协会账户
                if account.association_id != logic.association.id:
                    st = 1
                # 账户已加入其他部门
                elif account.department is not None:
                    st = 2
                else:
                    account.department = logic.department
                    account.save()
                    st = 0

            except:
                st = 3
            status[str(account.id)] = st

        return Result(status=status)

















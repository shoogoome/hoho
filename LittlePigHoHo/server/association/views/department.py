import json

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.enum.association.permission import AssociationPermissionEnum
from common.utils.helper.m_t_d import model_to_dict
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.department import DepartmentLogic
from ..logic.info import AssociationLogic
from ..models import AssociationDepartment


class DepartmentInfo(HoHoView):
    NOMAL_FILE = [
        'id', 'name', 'short_name', 'description', 'backlog', 'association',
        'association__id', 'association__name', 'master_administrator',
        'master_administrator__id', 'master_administrator__realname'
    ]

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
        dlogic = DepartmentLogic(self.auth, sid, aid, did)
        dlogic.check(AssociationPermissionEnum.DEPARTMENT_VIEW)

        return Result(data=model_to_dict(dlogic.department, self.NOMAL_FILE))

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
        alogic = AssociationLogic(self.auth, sid, aid)
        alogic.check(AssociationPermissionEnum.DEPARTMENT_CREATE)

        departmenr = AssociationDepartment.objects.create(
            name=params.str('name', desc="部门名称"),
            short_name=params.str('short_name', desc="缩写"),
            description=params.str('description', desc="描述", require=False, default=""),
            association=alogic.association
        )
        departmenr.master_administrator.add(self.auth.get_account())

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
        dlogic = DepartmentLogic(self.auth, sid, aid, did)
        dlogic.check(AssociationPermissionEnum.DEPARTMENT_MANAGE)
        department = dlogic.department

        if params.has('config'):
            permissions = params.dict('permissions', desc='配置信息')
            department.permissions = json.dumps(permissions)

        with params.diff(department):
            department.name = params.str('name', desc='部门名称')
            department.short_name = params.str('short_name', desc='名称缩写')

        department.save()

        return Result(id=department.id)

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
        dlogic.check(AssociationPermissionEnum.DEPARTMENT_DELETE)
        dlogic.department.delete()

        return Result(id=did)

# class DepartmentMatters(HoHoView):
#
#     @check_login
#     def post(self, request, sid, aid, did):
#         """
#         批量添加用户到指定部门
#         :param request:
#         :param sid:
#         :param aid:
#         :param did:
#         :return:
#         """
#         dlogic = DepartmentLogic(self.auth, sid, aid, did)
#         dlogic.check(AssociationPermissionEnum.DEPARTMENT_MANAGE)
#
#         params = ParamsParser(request.JSON)
#         ids = params.list('ids', desc='用户id')
#
#         for aid in ids:
#

import json

import requests
from django.db.models import Q

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
from common.entity.account.permission import AccountPermissionEntity
# from common.entity.account.permission import *
from common.enum.account.permission import AccountPermissionEnum
from common.enum.account.role import RoleEnum
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.info import AccountLogic
from ..models import Account
from common.enum.account.sex import SexEnum


class AccountView(HoHoView):

    STATUS = False

    def post(self, request):
        """
        注册账户 or 登陆账户
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        code = params.str('token', desc='验证ID')
        openid, session = self.get_openid(code)
        client_auth_mode = self.request.META.get('HTTP_HOHO_AUTH_MODEL') == "client"

        accounts = Account.objects.filter_cache(temp_access_token=openid)
        if len(accounts) == 0:
            try:
                nickname = params.str('nickname', desc='昵称')
                sex = params.int('sex', desc='性别')
                account = Account.objects.create(
                    realname=nickname,
                    nickname=nickname,
                    sex=sex,
                    temp_access_token=openid,
                    role=int(RoleEnum.DIRECTOR),
                    permissions=AccountPermissionEntity().dumps(),
                )
                _id = account.id
            except:
                raise AccountInfoExcept.account_filter_error()
        else:
            account = accounts[0]
            _id = account.id
        # 更新数据
        self.auth.set_account(account)
        # 载入登陆信息
        if client_auth_mode:
            return Result(data={
                "id": _id,
                "token": self.auth.create_token()
            }, association_id=self.auth.get_association_id())

        self.auth.set_account(account)
        self.auth.set_session()

        return Result(id=_id)

    @check_login
    def get(self, request, aid=''):
        """
        获取用户信息
        :param request:
        :param aid:
        :return:
        """
        if self.STATUS:
            logic = AccountLogic(self.auth, self.auth.get_account())
        else:
            # 权限控制
            logic = AccountLogic(self.auth, aid)
            # logic.check(AccountPermissionEnum.VIEWS)

        return Result(data=logic.get_account_info(), association_id=self.auth.get_association_id())

    @check_login
    def put(self, request, aid=''):
        """
        修改用户自身信息 or 管理员修改用户信息
        :param request:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JOSN)
        is_admin = False

        if self.auth.get_account().role == int(RoleEnum.ADMIN):
            alogic = AccountLogic(self.auth, aid)
            account = alogic.account
            is_admin = True
        else:
            account = self.auth.get_account()

        with params.diff(account):
            account.nickname = params.str('nickname', desc='昵称')
            account.realname = params.str('realname', desc='真实名称')
            account.sex = params.int('sex', desc='性别')
            account.email = params.str('email', desc='邮箱')
            account.phone = params.str('phone', desc='电话号码')
            account.motto = params.str('motto', desc='一句话留言')
            if is_admin and params.has('permission'):
                account.permissions = json.dumps(params.dict('permissions', desc='权限'))

        account.save()

        return Result(id=account.id, association_id=self.auth.get_association_id())

    def get_openid(self, code):
        """
        获取openid
        :return:
        """
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
            "wxefe392b88181200a",
            "3296b8d643b9a6e8603f18dec0df265c",
            code
        )

        response = requests.get(url)
        token = json.loads(response.text)

        if token.get('errcode', 0) != 0:
            raise AccountInfoExcept.token_error(token.get('errmsg', '未知错误'))

        return token.get('openid', ''), token.get('session_key', '')


class InfoView(HoHoView):

    LIST = False

    @check_login
    def get(self, request, aid):
        """
        提权（创建协会权限）or 获取用户列表
        :param request:
        :param aid:
        :return:
        """
        if not self.LIST:
            # 权限控制
            alogic = AccountLogic(self.auth, aid)
            if self.auth.get_account().role != int(RoleEnum.ADMIN):
                raise AccountInfoExcept.no_permission()

            permissions = AccountPermissionEntity.parse(alogic.account.permissions)
            permissions.create = True
            alogic.account.permissions = permissions.dumps()
            alogic.account.save()

            return Result(id=alogic.account.id, association_id=self.auth.get_association_id())

        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        accounts = Account.objects.values('id', 'update_time').all()

        if params.has('key'):
            key = params.str('key', desc='关键字 email 昵称 真实姓名 联系电话')
            accounts = accounts.filter(
                Q(email__contains=key) |
                Q(nickname__contains=key) |
                Q(realname__contains=key) |
                Q(phone__contains=key)
            )

        if params.has('role'):
            accounts = accounts.filter(role=params.int('role', desc='身份角色'))

        @slicer(accounts, limit=limit, page=page)
        def get_account_list(obj):
            return obj

        accounts, pagination = get_account_list()
        return Result(accounts=accounts, pagination=pagination, association_id=self.auth.get_association_id())

    def post(self, request):
        """
        批量获取用户信息
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = AccountLogic(self.auth)

        ids = params.list('ids', desc='id列表')
        accounts = Account.objects.get_many(ids=ids)

        data = []
        for account in accounts:
            try:
                logic.account = account
                data.append(logic.get_account_info())
            except:
                pass

        return Result(data=data, association_id=self.auth.get_association_id())


# !!!!! 仅仅为开发使用 !!!!!
class Login(HoHoView):

    def post(self, request):
        """
        开发登陆接口
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        code = params.str('token', desc='验证ID')

        accounts = Account.objects.filter(temp_access_token=code)
        if not accounts.exists():
            try:
                account = Account.objects.create(
                    temp_access_token=code,
                    role=int(RoleEnum.DIRECTOR),
                    permissions=AccountPermissionEntity().dumps(),
                )
            except:
                raise AccountInfoExcept.account_filter_error()
        else:
            account = accounts[0]
        # 载入登陆信息
        self.auth.set_account(account)
        self.auth.set_session()

        return Result(id=account.id, association_id=self.auth.get_association_id())

    def get(self, request):
        """
        切换协会id
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        code = params.int('association_id', desc='协会id')

        try:
            self.auth.update_association_id(code)
        except:
            raise AccountInfoExcept.error()

        return Result(id=code, association_id=code)

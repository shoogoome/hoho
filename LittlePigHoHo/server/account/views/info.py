import json

from common.core.auth.check_login import check_login
from common.core.http.view import HoHoView
# from common.entity.account.permission import *
from common.enum.account.permission import AccountPermissionEnum
from common.enum.account.role import RoleEnum
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.m_t_d import model_to_dict
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
from ..logic.info import AccountLogic
from ..models import Account
from common.entity.account.permission import AccountPermissionEntity
import requests
from common.entity.account.permission import AccountPermissionEntity


class AccountView(HoHoView):
    NORMAL_FILES = [
        'nickname', 'realname', 'sex', 'avator', 'motto', 'temp_access_token', 'permissions'
    ]

    STATUS = False

    def post(self, request):
        """
        注册账户 o登陆账户
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        code = params.str('token', desc='验证ID')
        openid, session = self.get_openid(code)
        client_auth_mode = self.request.META.get('hoho-auth-model') == "client"

        accounts = Account.objects.filter(temp_access_token=openid)
        if not accounts.exists():
            if self.STATUS:
                return Result(status=False)
            try:
                account = Account.objects.create(
                    realname=params.str('realname', desc='真实姓名'),
                    nickname=params.str('realname', desc='真实姓名'),
                    phone=params.str('phone', desc='电话号码'),
                    email=params.str('email', desc='邮箱', require=False, default=""),
                    sex=params.int('sex', desc='性别', require=False, default=0),
                    motto=params.str('motto', desc='一句话留言', require=False, default=""),
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
        # 载入登陆信息
        if client_auth_mode:
            return Result({
                "id": _id,
                "status": True,
                "token": self.auth.create_token()
            })

        self.auth.set_account(account)
        self.auth.set_session()
        if self.STATUS:
            return Result({
                "id": _id,
                "status": True
            })

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
            logic.check(AccountPermissionEnum.VIEWS)

        return Result(model_to_dict(logic.account, self.NORMAL_FILES))

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
            account.nickname = params.str('realname', desc='真实名称')
            account.realname = params.str('realname', desc='真实名称')
            account.sex = params.int('sex', desc='性别')
            account.email = params.str('email', desc='邮箱')
            account.phone = params.str('phone', desc='电话号码')
            account.motto = params.str('motto', desc='一句话留言')
            if is_admin and params.has('permission'):
                account.permissions = json.dumps(params.dict('permissions', desc='权限'))

        account.save()

        return Result(id=account.id)

    def get_openid(self, code):
        """
        获取openid
        :return:
        """
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
            "wx9fdb93e16d9b7154",
            "9d3adbb76f7962828d3e2b33eb74bc5b",
            code
        )

        response = requests.get(url)
        token = json.loads(response.text)

        if token.get('errcode', 0) != 0:
            raise AccountInfoExcept.token_error(token.get('errmsg', '未知错误'))

        return token.get('openid', ''), token.get('session_key', '')


class InfoView(HoHoView):

    @check_login
    def get(self, request, aid):
        """
        提权（创建协会权限）
        :param request:
        :param aid:
        :return:
        """
        # 权限控制
        alogic = AccountLogic(self.auth, aid)
        if self.auth.get_account().role != int(RoleEnum.ADMIN):
            raise AccountInfoExcept.no_permission()

        permissions = AccountPermissionEntity.parse(alogic.account.permissions)
        permissions.set_value('create', True)
        alogic.account.permissions = permissions.dumps()
        alogic.account.save()

        return Result(id=alogic.account.id)

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

        return Result(id=account.id)



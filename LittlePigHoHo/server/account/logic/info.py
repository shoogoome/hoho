import json

from common.enum.account.permission import AccountPermissionEnum
from common.enum.account.role import RoleEnum
from common.exceptions.account.info import AccountInfoExcept
from server.account.models import Account
from common.utils.helper.m_t_d import model_to_dict


class AccountLogic(object):

    NORMAL_FILES = [
        'nickname', 'realname', 'sex', 'avator', 'motto', 'permissions'
    ]

    def __init__(self, auth, aid='', thown=True):
        """
        INIT
        :param auth:
        :param aid:
        :param thown:
        """
        self.auth = auth
        if isinstance(aid, Account):
            self.account = aid
        else:
            self.account = self.get_account(aid, thown)

    def get_account(self, aid, thown):
        """
        获取账户model
        :return:
        """
        if aid is None or aid == '':
            return
        account = Account.objects.get_once(pk=aid)
        if thown and account is None:
            raise AccountInfoExcept.account_filter_error()
        return account

    def get_account_info(self):
        """
        获取账户信息
        :return:
        """
        return model_to_dict(self.account, self.NORMAL_FILES)

    def check(self, *permission):
        """
        权限处理
        :param permission:
        :return:
        """
        if self.auth.get_account().role == int(RoleEnum.ADMIN):
            return True
        if not AccountLogic.inspect(self.auth.get_account(), self.account, *permission):
            raise AccountInfoExcept.no_permission()

    @staticmethod
    def inspect(account, d_account=None, *permission):
        """
        检查权限
        :param account:
        :param d_account:
        :param permission:
        :return:
        """
        if AccountPermissionEnum.VIEWS in permission:
            if d_account is None:
                return False
            # 性能极低 等待优化
            auth_association = [aid for aid in account.association]
            account_association = [aid for aid in d_account.association]
            if len([i for i in auth_association if i in account_association]) > 0:
                return True

        if AccountPermissionEnum.CREATE_ASSOCIATION in permission:
            a_permission = json.loads(account.permissions)
            if a_permission.get('create', False):
                return True

        return False

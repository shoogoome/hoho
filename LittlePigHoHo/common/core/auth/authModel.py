from server.account.models import Account
from common.constants.params import *
from common.utils.hash.signatures import session_signature


class Authorization(object):

    def __init__(self, **kwargs):
        """
        INIT
        :param kwargs:
        """

    def is_login(self):
        """
        判断登陆与否
        :return:
        """
        ...

    def get_account(self):
        """
        获取账户model
        :return:
        """
        ...

    def set_account(self):
        """
        设置账户
        :return:
        """
        ...


class HoHoAuthorization(Authorization):

    def __init__(self, **kwargs):
        """
        HoHo授权
        :param kwargs:
        """
        super(HoHoAuthorization, self).__init__(**kwargs)
        self._is_login = False
        self._account = None

    def is_login(self):
        """
        返回登陆情况
        :return:
        """
        return self._is_login

    def get_account(self):
        """
        返回账户model
        :return:
        """
        return self._account

    def set_account(self, account):
        """
        设置账户model
        :param account:
        :return:
        """
        self._account = account
        pass

    @staticmethod
    def fetch_account_by_id(aid):
        """
        id查询账户model
        :param aid:
        :return:
        """
        try:
            return Account.objects.get(id=aid)
        except:
            return None

    def set_login_status(self, account_id):
        """
        挂起用户信息
        :param account_id:
        :return:
        """
        if account_id is not None:
            account = HoHoAuthorization.fetch_account_by_id(account_id)
            if account is not None:
                self._is_login = True
                self._account = account
                return True

        return False


class HoHoAuthAuthorization(HoHoAuthorization):

    def __init__(self, request, view):
        """
        auth验证
        :param request:
        :param view:
        """
        super(HoHoAuthAuthorization, self).__init__(request=request, view=view)
        self.request = request
        self.view = view
        self.load_from_session()

    def load_from_session(self):
        """
        载入登陆信息
        :return:
        """
        # 读取用户id
        account_id = self.request.session.get(HOHOAUTHSESSION, '')
        # 挂起登陆信息
        self.set_login_status(account_id)


    def set_session(self):
        """
        设置登陆信息
        :return:
        """
        if self._account is None:
            return False

        self.request.session[HOHOAUTHSESSION] = self._account.id
        # 产生登陆签名
        sign = session_signature(self._account.id)

        self.view.set_cookie(
            key=HOHOAUTHSIGN,
            value=sign,
        )

        return True










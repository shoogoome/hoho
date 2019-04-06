

from common.exceptions.account.info import AccountInfoExcept
from common.enum.account.role import RoleEnum

def administrators(fun):

    def wrapper(*args, **kwargs):
        """
        过滤非管理员用户
        :param args:
        :param kwargs:
        :return:
        """
        self = args[0]
        if self.auth.get_account().role == int(RoleEnum.ADMIN):
            return fun(*args, **kwargs)
        raise AccountInfoExcept.no_permission()

    return wrapper
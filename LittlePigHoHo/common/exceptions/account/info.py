from ..base import HoHoExceptBase

class AccountInfoExcept(HoHoExceptBase):

    @classmethod
    def account_filter_error(cls):
        return cls("差无此账户")

    @classmethod
    def no_permission(cls):
        return cls("无权限执行此操作")

    @classmethod
    def promotion_authority_error(cls):
        return cls("提权失败")

    @classmethod
    def is_not_login(cls):
        return cls("尚未登陆")

    @classmethod
    def token_error(cls, errmsg="get token error"):
        return cls(errmsg)

    @classmethod
    def error(cls):
        return cls("操作失败")

    @classmethod
    def secret_key_error(cls):
        return cls("密钥错误")

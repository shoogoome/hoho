from server.school.logic.info import SchoolLogic
from ..models import AssociationAccount
from common.exceptions.association.info import AssociationExcept
from .info import AssociationLogic
from common.utils.helper.m_t_d import model_to_dict

class AssociationAccountLogic(AssociationLogic):

    FIELD = [
        'nickanme', 'association', 'association__id', 'association__name',
        'department', 'department__id', 'department__name', 'role',
        'permissions', 'retire'
    ]

    def __init__(self, auth, sid, aid, acid=""):
        """
        协会人事逻辑
        :param auth:
        :param sid:
        :param aid:
        :param acid:
        """
        super(AssociationAccountLogic, self).__init__(auth, sid, aid)

        if isinstance(acid, AssociationAccount):
            self.other_account = aid
        else:
            self.other_account = self.get_account(acid)


    def get_account(self, acid):
        """
        获取协会人事model
        :param acid:
        :return:
        """
        if acid == "" or acid is None:
            return
        account = AssociationAccount.objects.get_once(pk=acid)
        if account is None or account.association_id != self.association.id:
            raise AssociationExcept.not_account()

        return account


    def get_account_info(self):
        """
        获取用户信息
        :return:
        """
        return model_to_dict(self.other_account, fields=self.FIELD)




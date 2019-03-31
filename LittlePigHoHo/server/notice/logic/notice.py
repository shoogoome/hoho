from server.association.logic.info import AssociationLogic
from ..models import AssociationNotice
from common.exceptions.notice.info import NoticeInfoExcept
from common.utils.helper.m_t_d import model_to_dict


class NoticeLogic(AssociationLogic):

    FIELD = [
        'author', 'author__id', 'author__nickname', 'association', 'association__id',
        'department', 'department__id', 'title', 'content', 'start_time', 'end_time',
        'update_time'
    ]

    def __init__(self, auth, sid, aid, nid=""):
        """
        通知逻辑
        :param auth:
        :param sid:
        :param aid:
        :param nid:
        """
        super(NoticeLogic, self).__init__(auth, sid, aid)

        if isinstance(nid, AssociationNotice):
            self.notice = nid
        else:
            self.notice = self.get_notice(nid)

    def get_notice(self, nid):
        """
        获取通知model
        :param nid:
        :return:
        """
        if nid == "" or nid is None:
            return
        notice = AssociationNotice.objects.get_once(pk=nid)
        if notice is None or notice.association_id != self.association.id:
            raise NoticeInfoExcept.no_notice()

        return notice


    def get_notice_info(self):
        """
        获取通知信息
        :return:
        """
        return model_to_dict(self.notice, self.FIELD)











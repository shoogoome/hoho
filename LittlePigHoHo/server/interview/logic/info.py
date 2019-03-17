
from ..models import *
from server.school.models import School
from server.school.logic.info import SchoolLogic
from server.association.logic.info import AssociationLogic
from server.association.models import Association
from common.exceptions.interview.info import InterviewInfoExcept


class RegistrationLogic(object):

    def __init__(self, auth, sid, aid, rid='', model=False, throw=False):
        """
        INIT
        :param auth:
        :param sid:
        :param aid:
        :param rid:
        :param model:
        :param throw:
        """
        self.auth = auth
        self.throw = throw
        if isinstance(sid, SchoolLogic):
            self.school_logic = sid
            self.school = self.school_logic.school
        elif isinstance(sid, School):
            self.school_logic = SchoolLogic(self.auth, sid)
            self.school = sid
        else:
            self.school_logic = SchoolLogic(self.auth, sid)
            self.school = self.school_logic.school
        if isinstance(aid, AssociationLogic):
            self.association_logic = aid
            self.association = self.association_logic.association
        elif isinstance(aid, Association):
            self.association_logic = AssociationLogic(self.auth, self.school_logic, aid)
            self.association = aid
        else:
            self.association_logic = AssociationLogic(self.auth, self.school_logic, aid)
            self.association = self.association_logic.association
        if model:
            self.registration_template = self.get_registration_template(rid)
        else:
            self.registration = self.get_registration(rid)

    def get_registration(self, rid):
        """
        获取报名表model
        :param rid:
        :return:
        """
        if rid == "" or rid is None:
            return
        registration = Registration.objects.get_once(id=rid)
        if registration is None and self.throw:
            raise InterviewInfoExcept.no_registration()
        return registration

    def get_using_template(self):
        """
        获取启用模板
        :return:
        """
        template = RegistrationTemplate.objects.filter(
            association=self.association, using=True)
        if not template.exists():
            raise InterviewInfoExcept.no_registration_template()
        return template[0]

    def using_template(self):
        """
        启用模板
        :return:
        """
        if self.registration_template is None: return
        registration_templat = RegistrationTemplate.objects.filter(
            association=self.association, using=True)
        if registration_templat.exists():
            registration_templat[0].using = False
            registration_templat[0].save()
        self.registration_template.using = True
        self.registration_template.save()

    def nouse_template(self):
        """
        不使用模板
        :return:
        """
        if self.registration_template is None: return
        self.registration_template.using = False

    def get_registration_template(self, rid):
        """
        获取报名表模板model
        :param rid:
        :return:
        """
        if rid == "" or rid is None: return
        registration_template = RegistrationTemplate.objects.filter(id=rid, association=self.association)
        if not registration_template.exists():
            if self.throw:
                raise InterviewInfoExcept.no_registration_template()
            return None
        return registration_template[0]



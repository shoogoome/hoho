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
from server.association.models import AssociationAccount, Association
import time
from common.core.auth.check_login import check_login


class AccountDashboard(HoHoView):

    @check_login
    def get(self, request):
        """
        获取相关事项
        :param request:
        :return:
        """
        # 获取所有参加协会账户
        accounts = AssociationAccount.objects.filter(account=self.auth.get_account())

        _time = time.time()

        data = {
            "notices": {},
            "tasks": {}
        }
        for account in accounts:
            # 获取 协会信息
            association = account.association
            # 构造通知信息
            notices = association.associationnotice_set.values('title', 'content', 'start_time', 'end_time').filter(end_time__lte=_time)
            data['notices'][association.name] = [notice for notice in notices]
            # 构造任务信息
            tasks = account.associationtaskreport_set.values(
                'task__title', 'task__content', 'task__start_time', 'task__end_time'
            ).filter(complete=False)
            data['tasks'][association.name] = [{
                "title": task.get('task__title', ""),
                "content": task.get('task__content', ""),
                "start_time": task.get('task__start_time', ""),
                "end_time": task.get('task__end_time', "")
            } for task in tasks]

        return Result(data=data, association_id=self.auth.get_association_id())











# -*- coding: utf-8 -*-
# coding: utf-8
from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from rediscluster import StrictRedisCluster
from LittlePigHoHo.settings import config_redis_cluster
import pickle
import base64

class Command(BaseCommand):

    # 获取redis集群配置
    db_configs = [v for _, v in config_redis_cluster.items()]

    def handle(self, *args, **options):
        """
        集群测试
        :param args:
        :param options:
        :return:
        """
        print("connect...")
        re = StrictRedisCluster(startup_nodes=self.db_configs, decode_responses=True, password='littlepighoho17**')

        re.set("11231", "123123")


        # print("success")
        # from server.account.models import Account
        # account = Account.objects.get(id=102)
        # print(account.id)
        #
        # pickled = pickle.dumps(account)
        # b64encoded = base64.b64encode(pickled).decode('latin1')
        # re.set("account:1", b64encoded)
        #
        # ac = re.get('account:1')
        # print(pickle.loads(base64.b64decode(ac.encode('latin1'))))


        # b = Account.objects.get_once(pk=102)
        # print(b.encode())





from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from server.account.models import Account
import requests
from faker import Faker
import json
import random

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        创建测试数据
        :param args:
        :param options:
        :return:
        """
        fake = Faker(locale='zh_CN')

        for i in range(3, 102):
            p = fake.profile()
            # Account.objects.create(
            #     nickname=p.get('name'),
            #     realname=p.get('name'),
            #     temp_access_token=i
            # )

            s = requests.session()
            response = s.post("http://hoho.server.net/accounts/register/this/is/jiekou/useing/to/kaifa", json={
                "token": 121
            })
            print(response.text)
            #
            # response = s.post("http://hoho.server.net/schools/1/associations/1/accounts?debug=1", json={
            #     "choosing_code": "20535904"
            # })
            #
            # print(response.status_code)

            # response = s.get("http://hoho.server.net/schools/1/associations/1/attendances/1/sign?debug=1&lx=1&ly=1")
            #
            # print(response.content)

            ss = ["A", "B", "C"]

            response = s.post("http://hoho.server.net/schools/1/associations/1/appraisings/scores?debug=1", json={
                "target_id": i,
                "content": {
                    "1": random.choice(ss),
                    "2": random.choice(ss)
                }
            })

            print(response.text)


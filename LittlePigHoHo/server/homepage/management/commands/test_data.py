from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from server.account.models import Account
import requests
from faker import Faker
import json
import random


school_name = [
    ("北京师范大学", "bnu"),
    ("北京理工大学", "sdhfwoehfwe"),
    ("北京师范大学珠海分校", "bnuz"),
]



class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        创建测试数据
        :param args:
        :param options:
        :return:
        """
        fake = Faker(locale='zh_CN')
        # 创建账户信息
        for i in range(100):
            p = fake.profile()
            Account.objects.create(
                nickname=p.get('name'),
                realname=p.get('name'),
                temp_access_token=i
            )
            print("[*] create account success")

        # 创建学校
        for i in range(3):
            # 会话session
            s = requests.session()
            response = s.post("http://hoho.server.net/accounts/register/this/is/jiekou/useing/to/kaifa", json={
                "token": i
            })
            if response.status_code == 200:
                print("[*] login success...")

            name = school_name[i]
            url = "http://hoho.server.net/schools?debug=1"
            response = s.post(url=url, json={
                "name": name[0],
                "short_name": name[1],
                "description": ""
            })
            if response.status_code == 200:
                print("[*] create school success...")
            else:
                print("[!] create school fail...")

            #
            # response = s.post("http://hoho.server.net/schools/1/associations/1/accounts?debug=1", json={
            #     "choosing_code": "20535904"
            # })
            #
            # print(response.status_code)

            # response = s.get("http://hoho.server.net/schools/1/associations/1/attendances/1/sign?debug=1&lx=1&ly=1")
            #
            # print(response.content)

            # ss = ["A", "B", "C"]
            #
            # response = s.post("http://hoho.server.net/schools/1/associations/1/appraisings/scores?debug=1", json={
            #     "target_id": i,
            #     "content": {
            #         "1": random.choice(ss),
            #         "2": random.choice(ss)
            #     }
            # })
            #
            # print(response.text)


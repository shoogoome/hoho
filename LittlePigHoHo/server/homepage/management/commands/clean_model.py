from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from server.account.models import Account
from server.association.models import Association

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        创建测试数据
        :param args:
        :param options:
        :return:
        """
        Association.objects.all().delete()

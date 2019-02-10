
from django.http import *


def home(request):
    """
    LittlePigHoHo首页
    :param request:
    :return:
    """
    return HttpResponse(
        "<association href=\"http://www.miitbeian.gov.cn\" target=\"_blank\">粤ICP备18139679号</association>")
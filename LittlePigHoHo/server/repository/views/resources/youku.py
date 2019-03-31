from common.core.http.view import HoHoView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import Result
import requests
import json
from ...logic.redis import ResourcesRedisFactory

class Resources(HoHoView):


    def get(self, request):
        """
        获取youku视频列表
        :param request:
        :return:
        """
        redis = ResourcesRedisFactory()
        params = ParamsParser(request.GET)
        key = params.str('key', desc="key")
        name = "youku:" + key

        if redis.exists(name):
            result = redis.lrange(name)
        else:
            url = "https://tip.soku.com/search_tip_1?jsoncallback=XBox.kUpdate&query={}&site=14&rm=C860B2D5BD8000015EF1A4007180F020-3&h=9".format(
                key
            )
            response = requests.get(url)
            result = json.loads(response.text.split('kUpdate(')[-1][:-1])['r']
            result = [i['w'] for i in result]
            redis.lpushs(name, result)

        return Result(result)

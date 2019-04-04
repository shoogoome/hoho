from common.core.dao.redis import RedisFactory



class AppraisingRedis(RedisFactory):
    
    def __init__(self):
        super(AppraisingRedis, self).__init__("appraising", 4)

    def hmset(self, name, data, expire=604800):
        """
        存储一周数据
        :param name:
        :param data:
        :param expire:
        :return:
        """
        self.redis.hmset(self._build_name(name), data)
        self.redis.expire(self._build_name(name), expire)



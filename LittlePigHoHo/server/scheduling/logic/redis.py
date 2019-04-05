from common.core.dao.redis import RedisFactory


class SchedulingRedis(RedisFactory):

    def __init__(self):
        """排班缓存   1月"""
        super(SchedulingRedis, self).__init__("scheduling", 5, expire=2592000)




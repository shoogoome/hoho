from common.core.dao.redis import RedisClusterFactory



class SchedulingRedis(RedisClusterFactory):

    def __init__(self):
        """排班缓存   1月"""
        super(SchedulingRedis, self).__init__("scheduling", expire=2592000)
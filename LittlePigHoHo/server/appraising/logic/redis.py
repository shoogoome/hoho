from common.core.dao.redis import RedisClusterFactory



class AppraisingRedis(RedisClusterFactory):

    def __init__(self):
        """评优缓存  一周"""
        super(AppraisingRedis, self).__init__("appraising", 604800)
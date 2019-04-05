from common.core.dao.redis import RedisFactory



class AppraisingRedis(RedisFactory):
    
    def __init__(self):
        """评优缓存  一周"""
        super(AppraisingRedis, self).__init__("appraising", 4, 604800)


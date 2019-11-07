from common.core.dao.redis import RedisClusterFactory



class NoticeRedis(RedisClusterFactory):
    
    def __init__(self):
        """
        通知缓存 半年
        """
        super(NoticeRedis, self).__init__("notice", 15552000)





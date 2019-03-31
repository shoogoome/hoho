from common.core.dao.redis import RedisFactory



class ResourcesRedisFactory(RedisFactory):


    def __init__(self):
        """
        资源缓存工厂
        """
        super(ResourcesRedisFactory, self).__init__("resources", 3)


from common.core.dao.redis import RedisClusterFactory


class AttendanceRedisFactory(RedisClusterFactory):

    def __init__(self):
        super(AttendanceRedisFactory, self).__init__("Attendance", 31536000)

    def hset(self, name, key, value, expire=31536000):
        """
        添加hash 一年缓存
        :param name:
        :param key:
        :param value:
        :param expire:
        :return:
        """
        self.redis_cluster.hset(self._build_name(name), key, value)
        # 第一次创建key时设定过期时间
        if self.redis_cluster.ttl(self._build_name(name)) == -1:
            self.redis_cluster.expire(self._build_name(name), expire)
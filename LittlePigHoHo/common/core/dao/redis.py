# -*- coding: utf-8 -*-
# coding:utf-8
import redis
from django.conf import settings

redis_pool = {}

def get_redis_conn(db=1):
    """
    建立Redis连接
    :param db: 0-session  1-考勤  2-数据库缓存  3-资源缓存  4-评优缓存
    :return:
    """
    if db not in redis_pool.keys():
        redis_pool[db] = redis.ConnectionPool(
            host=settings.REDIS_CONFIG_HOST,
            port=settings.REDIS_CONFIG_PORT,
            password=settings.REDIS_CONFIG_PASSWORD,
            db=db
        )

    return redis.StrictRedis(connection_pool=redis_pool[db])


class RedisFactory(object):


    def __init__(self, name="default", db=1, expire=86400):
        """
        缓存工厂
        :param name: 默认缓存key域
        :param db: redis数据库编号
        """
        self.name = name
        self.redis = get_redis_conn(db)
        self.expire=expire

    def set(self, name, value):
        """
        set方法
        :param name:
        :param value:
        :return:
        """
        self.redis.set(self._build_name(name), value, ex=self.expire)

    def get(self, name):
        """
        get方法
        :param name:
        :return:
        """
        return self.redis.get(self._build_name(name))

    def hgetall(self, name):
        """
        获取全部name对应hash内容
        :param name:
        :return:
        """
        return self.redis.hgetall(self._build_name(name))

    def hget(self, name, key):
        """
        获取name对应key对应
        :param name:
        :param key:
        :return:
        """
        return self.redis.hget(self._build_name(), key)

    def hmset(self, name, data):
        """
        添加hash入缓存 一天缓存时间
        :param name:
        :param data:
        :return:
        """
        self.redis.hmset(self._build_name(name), data)
        self.redis.expire(self._build_name(name), self.expire)

    def hset(self, name, key, value):
        """
        添加hash 一天缓存
        :param name:
        :param key:
        :param value:
        :return:
        """
        self.redis.hset(self._build_name(name), key, value)
        self.redis.expire(self._build_name(name), self.expire)

    def lpushs(self, name, data):
        """
        数组批量缓存
        :param name:
        :param data:
        :param expire:
        :return:
        """
        name = self._build_name(name)
        [(self.redis.rpush(name, i.encode()), self.redis.expire(name, self.expire)) for i in data]

    def lrange(self, name):
        """
        获取全数组
        :param name:
        :return:
        """
        data = self.redis.lrange(self._build_name(name), 0, -1)
        return [i.decode() for i in data]


    def exists(self, name):
        """
        判断存在与否
        :param name:
        :return:
        """
        return self.redis.exists(self._build_name(name))

    def ttl(self, name):
        """
        返回国企过期时间
        :param name:
        :return:
        """
        return self.redis.ttl(self._build_name(name))

    def delete(self, name):
        """
        删除任意形式的键值
        :param name:
        :return:
        """
        self.redis.delete(self._build_name(name))

    def _build_name(self, *key):
        """
        构建 redis name
        :param key:
        :return:
        """
        return ':'.join([self.name, *key])


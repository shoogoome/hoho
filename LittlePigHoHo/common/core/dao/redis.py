# -*- coding: utf-8 -*-
# coding:utf-8
import redis
from django.conf import settings

redis_pool = {}

def get_redis_conn(db=1):
    """
    建立Redis连接
    :param db: 0-session  1-考勤  2-数据库缓存  3-资源缓存
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


    def __init__(self, name="default", db=1):
        """
        缓存工厂
        :param name: 默认缓存key域
        :param db: redis数据库编号
        """
        self.name = name
        self.redis = get_redis_conn(db)

    def set(self, name, value, expire=86400):
        """
        set方法
        :param name:
        :param value:
        :param expire:
        :return:
        """
        self.redis.set(self.build_name(name), value, ex=expire)

    def get(self, name):
        """
        get方法
        :param name:
        :return:
        """
        return self.redis.get(self.build_name(name))

    def hgetall(self, name):
        """
        获取全部name对应hash内容
        :param name:
        :return:
        """
        return self.redis.hgetall(self.build_name(name))

    def hmset(self, name, data, expire=86400):
        """
        添加hash入缓存 一天缓存时间
        :param name:
        :param data:
        :param expire:
        :return:
        """
        self.redis.hmset(self.build_name(name), data)
        self.redis.expire(self.build_name(name), expire)

    def lpushs(self, name, data, expire=86400):
        """
        数组批量缓存
        :param name:
        :param data:
        :param expire:
        :return:
        """
        name = self.build_name(name)
        [(self.redis.rpush(name, i.encode()), self.redis.expire(name, expire)) for i in data]

    def lrange(self, name):
        """
        获取全数组
        :param name:
        :return:
        """
        data = self.redis.lrange(self.build_name(name), 0, -1)
        return [i.decode() for i in data]


    def exists(self, name):
        """
        判断存在与否
        :param name:
        :return:
        """
        return self.redis.exists(self.build_name(name))

    def delete(self, name):
        """
        删除任意形式的键值
        :param name:
        :return:
        """
        self.redis.delete(self.build_name(name))

    def build_name(self, *key):
        """
        构建 redis name
        :param key:
        :return:
        """
        return ':'.join([self.name, *key])


# -*- coding: utf-8 -*-
# coding:utf-8
import redis
from django.conf import settings

redis_pool = {}

def get_redis_conn(db=2):
    """
    建立Redis连接
    :param db:
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

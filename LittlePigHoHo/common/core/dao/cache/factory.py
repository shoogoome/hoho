# -*- coding: utf-8 -*-
# coding:utf-8

from django.core.cache import cache


class HoHoCacheFactory(object):

    def __init__(self, key_list):
        """
        初始化
        :param key_list:
        设计上字段名会按照:
        类型: {model_cache, default_cache}
        数据表名: {model_table}
        数据集id: {object.id}
        """
        self.cache = cache
        if isinstance(key_list, list) or isinstance(key_list, tuple):
            self.key_list = ':'.join(key_list)
        elif key_list is not None:
            self.key_list = str(key_list)
        else:
            self.key_list = 'default_cache'

    def get_cache(self, key):
        """
        获取缓存信息
        :param key:
        :return:
        """
        l_key = self._build_key(key)
        return self.cache.get(l_key)

    def set_cache(self, key, value, expired=86400):
        """
        设置缓存（生命周期一天）
        :param key:
        :param value:
        :param expired:
        :return:
        """
        l_key = self._build_key(key)
        return self.cache.set(l_key, value, expired)

    def _build_key(self, key):
        """
        构建缓存字段名
        :return:
        """
        return "{}:{}".format(self.key_list, key)

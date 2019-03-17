from django.db.models import Manager
from .factory import HoHoCacheFactory


class HoHoModelManager(Manager):

    def get_once(self, lid):
        """
        缓存中获取一条记录
        若无则从数据库获取
        替代model中get方法
        :param lid:
        :return:
        """

        if lid is None or lid == "":
            return None
        # 获取数据表名
        table_name = self.model._meta.db_table
        # 初始化缓存
        cache = HoHoCacheFactory(('model_cache', table_name))
        # 尝试从缓存获取对象
        obj = cache.get_cache(lid)
        if obj is None:
            # 尝试从数据库中获取
            try:
                obj = super().get_queryset().get(id=id)
            except:
                return None
            cache.set_cache(lid, obj)
        return obj

    def get_many(self, ids):
        """
        get_once延伸
        :param ids:
        :return:
        """
        resule = []
        if isinstance(ids, list):
            for lid in ids:
                try:
                    resule.append(self.get_once(lid))
                except:
                    pass
        return resule





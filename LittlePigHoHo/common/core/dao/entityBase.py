import json
from .proptype import PropType

class EntityBase(object):
    """
    entityBase
    """

    EntityBaseFun = ['update', 'dump', 'parse', 'dumps']

    def __init__(self, **kwargs):
        """
        INIT
        """
        self.update(kwargs)

    def update(self, source):
        """
        参数写入类中
        :param source:
        :return:
        """
        self_keys = self.__dict__.keys()
        for key, val in source.items():
            if key not in self_keys:
                continue
            item = self.__getattribute__(key)
            if item is None: continue
            if isinstance(item, PropType):
                item._value = val
            else:
                self.__setattr__(key, val)

    def dump(self):
        """
        解析成员为字典
        :return:
        """
        tmp = {}
        for key, val in self.__dict__.items():
            if key[:2] == '__' or key[:1] == '_' or key in EntityBase.EntityBaseFun:
                continue
            if isinstance(val, PropType):
                tmp[key] = val.get_value()
            else:
                tmp[key] = val
        return tmp

    @classmethod
    def parse(cls, data):
        """
        解析
        :return:
        """
        data = json.loads(data)
        return cls(**data)

    def dumps(self):
        """
        解析成员为字典格式字符串
        :return:
        """
        return json.dumps(self.dump())

    def set_value(self, key, val):
        """
        设置val
        :param key:
        :param val:
        :return:
        """
        item = self.__getattribute__(key)
        if item is None:
            return
        if isinstance(item, PropType):
            item.set_value(val)
            self.__setattr__(key, item)
        else:
            self.__setattr__(key, val)

    def __getattribute__(self, key):
        """
        重写get函数
        :param key:
        :return:
        """
        try:
            return object.__getattribute__(self, key)
        except:
            return None

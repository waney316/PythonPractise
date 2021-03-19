## 自定义django orm
from numbers import Integral

# 属性描述符规定字段类型
class Field:
    pass

class IntField(Field):
    def __init__(self, db_column, min_value=None, max_value=None):
        self._value = None
        self.db_column = None
        self.min_value = min_value
        self.max_value = max_value

        # handler min_value or max_value is None
        if min_value is None or max_value is None:
            raise ValueError("must set intfield min_value and max_value")
        # handle min_value column
        if min_value is not None:
            if not isinstance(min_value, Integral):
                raise ValueError("min_value must int")
            elif min_value<0:
                raise ValueError("MIN_VALUE must gt 0")
        # handler max_value column
        if max_value is not None:
            if not isinstance(max_value, Integral):
                raise ValueError("max_value must int")
            elif max_value<0:
                raise ValueError("MAX_VALUE must gt 0")
        # hanlde min_value > max_value
        if min_value > max_value:
            raise ValueError("min_value must le max_value")
    def __get__(self, instance, owner):
        return self._value
    def __set__(self, instance, value):
        if not isinstance(value, Integral):
            raise ValueError("IntField need")
        if value < self.min_value or value > self.max_value:
            raise ValueError("value must between min_value~max_value")
        self.value = value

# 定义字符类型
class CharField(Field):
    def __init__(self, db_column, max_length=None):
        self._value = None
        self.db_column = db_column
        self.max_length = max_length

        if max_length is None:
            raise ValueError("must assign maxlength for charfield")

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("CharField need")
        if len(value) > self.max_length:
            raise ValueError("value len gt len of max_legth")
        self._value = value

# 元类注册属性
class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        fields = {}
        for k,v in attrs.items():
            if isinstance(v, Field):
                fields[k] = v
            # 获取meta信息
            attr_meta = attrs.get("Meta", None)
            _meta = {}
            db_table = name.lower()
            if attr_meta is not None:
                table = getattr(attr_meta, "db_tables", None)
                if table is not None:
                    db_table = table
            _meta["db_table"] = db_table
            attrs["fields"] = fields
            del attrs["Meta"]
            return super().__new__(cls, name, bases, attrs, **kwargs)


class BaseModel(metaclass=ModelMetaClass):
    def __init__(self, *args, **kwargs):
        for key,value in kwargs.items():
            setattr(self, key, value)
        return super(BaseModel, self).__init__()

    def save(self):
        pass
# 定义User Model
class User(BaseModel):
    def __init__(self):
        pass
    name = CharField(db_column="", max_length=32)
    age = IntField(db_column="", min_value=0, max_value=100)

    class Meta:
        pass

if __name__ == '__main__':
    user = User()
    user.name = "wangwei"
    user.age = 4


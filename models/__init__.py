import json

from utils import log


def save(data, path):
    """
    把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json.dumps() 将要写入的 dict/list 转化成 str
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    # json.loads() 将文件中的数据转化成 dict/list
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    # Model 是用于存储数据的基类
    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        """
        得到 存储文件 路径
        """
        # 得到 谁调用的 类的名字，用它给存储文件命名
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # 如果是 User 类调用 就相当于User(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        all 方法使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        find_by 方法 返回 满足条件的第一个 model
        """
        models = cls.all()
        for model in models:
            flag = 1
            for k, v in kwargs.items():
                if getattr(model, k) != v:
                    flag = 0
                    break
            if flag == 1:
                return model
        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        find_all 方法 返回 满足条件的所有的 models
        """
        models = cls.all()
        model_found = []
        for model in models:
            flag = 1
            for k, v in kwargs.items():
                if getattr(model, k) != v:
                    flag = 0
                    break
            if flag == 1:
                model_found.append(model)
        return model_found

    def save(self):
        """
        增加 或 更新 self
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        if self.id is None:
            log('models', models)
            if len(models) == 0:
                self.id = 1
            else:
                self.id = models[len(models) - 1].id + 1
            models.append(self)
            # __dict__ 是包含了对象所有属性和值的字典
            l = [m.__dict__ for m in models]
        else:
            l = [m.__dict__ for m in models]
            log('models to dicts', l)
            for m in l:
                log('m in l', m)
                if m['id'] == self.__dict__['id']:
                    log('m.items()', m.items())
                    for k in m:
                        log('k in m', k)
                        m[k] = self.__dict__[k]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        __repr__ 得到类的 字符串表达 形式
        print(u) 即 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
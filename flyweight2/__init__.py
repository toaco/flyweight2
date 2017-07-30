import copy
import operator
import pickle
import weakref

import types

__version__ = '0.0.2'


def new_method_proxy(func):
    def inner(self, *args):
        return func(getattr(self, '_target'), *args)

    return inner


class StaticMethod(staticmethod):
    def __call__(self, *args, **kw):
        return self.__func__(*args, **kw)


class ClassMethod(classmethod):
    def __call__(self, *args, **kw):
        return self.__func__(*args, **kw)


class Proxy(object):
    def __init__(self, target):
        object.__setattr__(self, '_target', target)

    def __getattr__(self, name):
        target = self._target

        attr = getattr(target, name)

        if callable(attr):
            attr = getattr(target.__class__, name)
            pool = getattr(target.__class__, '_pool')

            copied_target = copy.deepcopy(target)

            def func(*args, **kwargs):
                copied_target_ = copied_target
                result = attr(*args, **kwargs)
                key = copied_target_._key()
                if key not in pool:
                    pool[key] = copied_target_
                    object.__setattr__(self, '_target', copied_target_)
                else:
                    object.__setattr__(self, '_target', pool[key])
                return result

            if name in getattr(target.__class__, '_static_methods'):
                return StaticMethod(func)
            if name in getattr(target.__class__, '_class_methods'):
                return ClassMethod(func)
            else:
                return types.MethodType(func, copied_target)
        else:
            attr = getattr(target, name)
            return attr

    def __setattr__(self, key, value):
        target = self._target
        copied_target = copy.deepcopy(target)

        setattr(copied_target, key, value)

        key = copied_target._key()
        pool = getattr(target.__class__, '_pool')

        if key not in pool:
            pool[key] = copied_target
            object.__setattr__(self, '_target', copied_target)
        else:
            object.__setattr__(self, '_target', pool[key])

    __delattr__ = new_method_proxy(delattr)

    __str__ = new_method_proxy(str)
    __unicode__ = new_method_proxy(unicode)
    __nonzero__ = new_method_proxy(bool)

    __dir__ = new_method_proxy(dir)

    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)

    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


class FlyWeight2Meta(type):
    def __new__(mcs, name, parents, dct):
        static_methods = set()
        class_methods = set()

        for key, value in dct.iteritems():
            if isinstance(value, staticmethod):
                static_methods.add(key)
            elif isinstance(value, classmethod):
                class_methods.add(key)
        dct['_static_methods'] = static_methods
        dct['_class_methods'] = class_methods

        dct['_pool'] = weakref.WeakValueDictionary()

        def _key(self, *args, **kwargs):
            key = pickle.dumps(self)
            return key

        dct['_key'] = _key

        def __deepcopy__(self, memo):
            cls = self.__class__
            result = cls.__new__(cls)
            memo[id(self)] = result
            for k, v in self.__dict__.items():
                setattr(result, k, copy.deepcopy(v, memo))
            return result

        dct['__deepcopy__'] = __deepcopy__

        return super(FlyWeight2Meta, mcs).__new__(mcs, name, parents, dct)

    def __call__(cls, *args, **kwargs):
        pool = getattr(cls, '_pool')

        instance = super(FlyWeight2Meta, cls).__call__(*args, **kwargs)
        key = instance._key()

        if key in pool:
            return Proxy(pool[key])
        else:
            pool[key] = instance
            return Proxy(instance)

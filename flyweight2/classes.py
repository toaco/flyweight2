from flyweight2 import FlyWeight2Meta


class Object(object):
    __metaclass__ = FlyWeight2Meta


class List(list):
    __metaclass__ = FlyWeight2Meta


class Dict(dict):
    __metaclass__ = FlyWeight2Meta


class Set(set):
    __metaclass__ = FlyWeight2Meta

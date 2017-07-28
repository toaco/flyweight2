from flyweight2.classes import Object as Obj, List, Dict, Set


class Object(Obj):
    y = 0

    def __init__(self, x):
        self.x = x

    def update(self, value):
        self.x = value

    @classmethod
    def update_cls_attr_by_classmethod(cls, value):
        cls.y = value

    @staticmethod
    def update_cls_attr_by_staticmethod(value):
        Object.y = value

    def update_cls_attr_by_instancemethod(self, value):
        Object.y = value


obj_pool = getattr(Object, '_pool')


class TestObjectCreation(object):
    def test_not_create_object(self):
        assert len(obj_pool) == 0

    def test_create_object_1(self):
        a = Object(1)
        assert a.__class__ == Object
        assert type(a) != Object
        assert isinstance(a, object)

    def test_create_object_2(self):
        a = Object(1)

        assert a.x == 1
        assert len(obj_pool) == 1

    def test_create_object_3(self):
        a = Object(1)
        b = Object(1)

        assert a.x == 1
        assert b.x == 1
        assert len(obj_pool) == 1

    def test_create_object_4(self):
        a = Object(1)
        b = Object(2)

        assert a.x == 1
        assert b.x == 2
        assert len(obj_pool) == 2


class TestObjectUpdateByDirectlyAssign(object):
    def test_update_1(self):
        a = Object(1)
        b = Object(1)
        a.x = 1

        assert a.x == 1
        assert b.x == 1
        assert len(obj_pool) == 1

    def test_update_2(self):
        a = Object(1)
        b = Object(1)
        a.x = 2

        assert a.x == 2
        assert b.x == 1
        assert len(obj_pool) == 2

    def test_update_3(self):
        a = Object(1)
        b = Object(1)
        c = Object(2)
        a.x = 2

        assert a.x == 2
        assert b.x == 1
        assert c.x == 2
        assert len(obj_pool) == 2

    def test_update_class_attribute(self):
        a = Object(1)
        b = Object(1)
        a.y = 1

        assert a.y == 1
        assert b.y == 0
        assert len(obj_pool) == 2


class TestObjectUpdateByOtherWay(object):
    def test_update_by_method(self):
        a = Object(1)
        a.update(2)

        assert a.x == 2
        assert len(obj_pool) == 1

    def test_update_cls_attr_by_instancemethod(self):
        a = Object(1)
        b = Object(1)
        a.update_cls_attr_by_instancemethod(1)

        assert a.y == 1
        assert b.y == 1
        assert len(obj_pool) == 1

    def test_update_class_attribute_by_staticmethod(self):
        a = Object(1)
        b = Object(1)
        a.update_cls_attr_by_staticmethod(1)

        assert a.y == 1
        assert b.y == 1
        assert len(obj_pool) == 1

    def test_update_class_attribute_by_classmethod(self):
        a = Object(1)
        b = Object(1)
        a.update_cls_attr_by_classmethod(1)

        assert a.y == 1
        assert b.y == 1
        assert len(obj_pool) == 1


def test_list():
    list_pool = getattr(List, '_pool')

    a1 = List()
    a2 = List()
    a3 = List([1])

    assert a1 == []
    assert a2 == []
    assert a3[0] == 1
    assert len(list_pool) == 2

    a2.append(1)
    assert a1 == []
    assert a2[0] == 1
    assert a3[0] == 1
    assert len(list_pool) == 2


def test_dict():
    dict_pool = getattr(Dict, '_pool')

    a1 = Dict()
    a2 = Dict()
    a3 = Dict({1: 2})

    assert a1 == {}
    assert a2 == {}
    assert a3[1] == 2
    assert len(dict_pool) == 2

    a2.update({1: 2})
    assert a1 == {}
    assert a2[1] == 2
    assert a3[1] == 2
    assert len(dict_pool) == 2


def test_set():
    set_pool = getattr(Set, '_pool')

    a1 = Set()
    a2 = Set()
    a3 = Set({1})

    assert a1 == set()
    assert a2 == set()
    assert a3 == {1}
    assert len(set_pool) == 2

    a2.add(1)
    assert a1 == set()
    assert a2 == {1}
    assert a3 == {1}
    assert len(set_pool) == 2

import unittest
import util.classutils as utils


class TestInstantiateFunction(unittest.TestCase):

    def test_function_should_return_list(self):
        result = utils.instantiate([])
        assert isinstance(result, list)

    def test_empty_class_list_should_return_empty_list(self):
        result = utils.instantiate([])
        assert len(result) == 0

    def test_instantiate_should_return__MockClass_object(self):
        result = utils.instantiate([_MockClass])
        assert len(result) == 1
        assert type(result[0]) is _MockClass

    def test_instantiate_should_return_requested_class_instances(self):
        result = utils.instantiate([_MockClass, _MockClass1, _MockClass2])
        assert len(result) == 3
        assert type(result[0]) is _MockClass
        assert type(result[1]) is _MockClass1
        assert type(result[2]) is _MockClass2


class TestGetAllSubclassesFunction(unittest.TestCase):

    def test_get_all_subclasses_should_return_all__MockClass_subclasses(self):
        result = utils.get_all_subclasses(_MockClass)
        assert len(result) == 6
        assert _MockClass1 in result
        assert _MockClass2 in result
        assert _MockClass1A in result
        assert _MockClass1B in result
        assert _MockClass2A in result
        assert _MockClass2B in result

    def test_get_all_subclasses_should_return_all__MockClass1_subclasses(self):
        result = utils.get_all_subclasses(_MockClass1)
        assert len(result) == 2
        assert _MockClass1A in result
        assert _MockClass1B in result

    def test_get_all_subclasses_should_return_no_subclasses(self):
        result = utils.get_all_subclasses(_MockClass2A)
        assert len(result) == 0


class _MockClass(object):
    pass


class _MockClass1(_MockClass):
    pass


class _MockClass2(_MockClass):
    pass


class _MockClass1A(_MockClass1):
    pass


class _MockClass1B(_MockClass1):
    pass


class _MockClass2A(_MockClass2):
    pass


class _MockClass2B(_MockClass2):
    pass

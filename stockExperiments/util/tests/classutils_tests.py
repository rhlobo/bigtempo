import unittest
import util.classutils as utils


class TestInstantiateFunction(unittest.TestCase):

    def test_function_should_return_list(self):
        result = utils.instantiate([])
        assert isinstance(result, list)

    def test_empty_class_list_should_return_empty_list(self):
        result = utils.instantiate([])
        assert len(result) == 0

    def test_instantiate_should_return_MockClass_object(self):
        result = utils.instantiate([MockClass])
        assert len(result) == 1
        assert type(result[0]) is MockClass

    def test_instantiate_should_return_requested_class_instances(self):
        result = utils.instantiate([MockClass, MockClass1, MockClass2])
        assert len(result) == 3
        assert type(result[0]) is MockClass
        assert type(result[1]) is MockClass1
        assert type(result[2]) is MockClass2


class TestGetAllSubclassesFunction(unittest.TestCase):

    def test_get_all_subclasses_should_return_all_MockClass_subclasses(self):
        result = utils.get_all_subclasses(MockClass)
        assert len(result) == 6
        assert MockClass1 in result
        assert MockClass2 in result
        assert MockClass1A in result
        assert MockClass1B in result
        assert MockClass2A in result
        assert MockClass2B in result

    def test_get_all_subclasses_should_return_all_MockClass1_subclasses(self):
        result = utils.get_all_subclasses(MockClass1)
        assert len(result) == 2
        assert MockClass1A in result
        assert MockClass1B in result

    def test_get_all_subclasses_should_return_no_subclasses(self):
        result = utils.get_all_subclasses(MockClass2A)
        assert len(result) == 0


class MockClass(object):
    pass


class MockClass1(MockClass):
    pass


class MockClass2(MockClass):
    pass


class MockClass1A(MockClass1):
    pass


class MockClass1B(MockClass1):
    pass


class MockClass2A(MockClass2):
    pass


class MockClass2B(MockClass2):
    pass

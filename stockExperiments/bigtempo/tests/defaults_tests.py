import unittest
from mockito import mock, when, any as anyx, verify, verifyNoMoreInteractions

import bigtempo.defaults as defaults


class TestModuleFunctions(unittest.TestCase):

    def test_builder_should_return_instance_of_given_class(self):
        class Foo(object):
            pass

        result = defaults.builder(Foo)

        assert isinstance(result, Foo)

    def test_processingtask_factory_should_return_processing_task(self):
        instance = mock()
        dependencies = mock()
        lookback_period = mock()

        result = defaults.processingtask_factory(instance, dependencies, lookback_period)
        assert isinstance(result, defaults.DatasourceTask)


class TestDatasourceTask(unittest.TestCase):
    pass


class TestDataFrameDatasourceTask(unittest.TestCase):
    pass


class TestDatasourceContext(unittest.TestCase):

    def test_dependencies_should_return_dependencies_given_through_constructor_when_no_reference_is_passed(self):
        expected = object()

        task = defaults.DatasourceContext(expected)
        result = task.dependencies()

        assert result is expected

    def test_dependencies_should_return_specific_dependency_when_reference_is_specifyed(self):
        deps = {
            'a': 0,
            'b': 1,
            'c': 2
        }

        task = defaults.DatasourceContext(deps)
        result = task.dependencies('b')

        assert result is 1

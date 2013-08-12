import unittest
from mockito import mock, when, any as anyx, verify
import pandas

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

        result = defaults.processingtask_factory(instance, dependencies)
        assert isinstance(result, defaults.DataFrameDatasourceTask)


class TestDatasourceTask(unittest.TestCase):

    def test_process_should_process_dependencies(self):
        instance = mock()
        dependencies = {
            'a': mock(defaults.SimpleDatasourceTask),
            'b': mock(defaults.SimpleDatasourceTask),
            'c': mock(defaults.SimpleDatasourceTask),
        }

        defaults.SimpleDatasourceTask(instance, dependencies).process()

        verify(dependencies['a'], times=1).process()
        verify(dependencies['b'], times=1).process()
        verify(dependencies['c'], times=1).process()
        verify(instance, times=1).evaluate(anyx(dict))

    def test_process_should_receive_dependencies_process_results_as_context(self):
        class DatasourceMock():

            def evaluate(self, context):
                assert isinstance(context, dict)
                assert len(context) is 2
                assert context['a'] == '1'
                assert context['b'] == '2'

        dependencies = {
            'a': mock(defaults.SimpleDatasourceTask),
            'b': mock(defaults.SimpleDatasourceTask),
        }
        when(dependencies['a']).process().thenReturn('1')
        when(dependencies['b']).process().thenReturn('2')

        defaults.SimpleDatasourceTask(DatasourceMock(), dependencies).process()


class TestDataFrameDatasourceTask(unittest.TestCase):

    def test_process_should_process_dependencies(self):
        instance = mock()
        symbol = 'symbol'
        start = None
        end = None
        dependencies = {
            'a': mock(defaults.DataFrameDatasourceTask),
            'b': mock(defaults.DataFrameDatasourceTask),
            'c': mock(defaults.DataFrameDatasourceTask),
        }

        defaults.DataFrameDatasourceTask(instance, dependencies).process(symbol, start, end)

        verify(dependencies['a'], times=1).process(symbol, start, end)
        verify(dependencies['b'], times=1).process(symbol, start, end)
        verify(dependencies['c'], times=1).process(symbol, start, end)
        verify(instance, times=1).evaluate(anyx(defaults.DatasourceContext), symbol, start, end)

    def test_process_should_receive_dependencies_process_results_as_context(self):
        symbol = 'symbol'
        start = None
        end = None
        expected_a = pandas.DataFrame([1, 2, 3])
        expected_b = pandas.DataFrame([9, 8, 7])

        class DatasourceMock():

            def evaluate(self, context, s, ds, de):
                assert isinstance(context, defaults.DatasourceContext)
                deps = context.dependencies()
                assert isinstance(deps, dict)
                assert len(deps) is 2
                assert (deps['a'].values == expected_a.values).all()
                assert (deps['b'].values == expected_b.values).all()
                assert s == symbol
                assert ds == start
                assert de == end

        dependencies = {
            'a': mock(defaults.DataFrameDatasourceTask),
            'b': mock(defaults.DataFrameDatasourceTask),
        }
        when(dependencies['a']).process(symbol, start, end).thenReturn(expected_a)
        when(dependencies['b']).process(symbol, start, end).thenReturn(expected_b)

        defaults.DataFrameDatasourceTask(DatasourceMock(), dependencies).process(symbol, start, end)


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

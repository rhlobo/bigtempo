# -*- coding: utf-8 -*-


import pandas
import unittest

from mockito import mock, when, any as anyx, verify

import bigtempo.processors.dataframe_task as task


class TestModuleFunctions(unittest.TestCase):

    def test_processingtask_factory_should_return_processing_task(self):
        instance = mock()
        dependencies = mock()
        registration = mock()

        result = task.factory(instance, registration, dependencies)
        assert isinstance(result, task.DataFrameDatasourceTask)


class TestDataFrameDatasourceTask(unittest.TestCase):

    def test_process_should_process_dependencies(self):
        instance = mock()
        registration = mock()

        symbol = 'symbol'
        start = None
        end = None

        dependencies = {
            'a': mock(task.DataFrameDatasourceTask),
            'b': mock(task.DataFrameDatasourceTask),
            'c': mock(task.DataFrameDatasourceTask),
        }

        task.DataFrameDatasourceTask(instance, registration, dependencies).process(symbol, start, end)

        verify(dependencies['a'], times=1).process(symbol, start, end)
        verify(dependencies['b'], times=1).process(symbol, start, end)
        verify(dependencies['c'], times=1).process(symbol, start, end)
        verify(instance, times=1).evaluate(anyx(task.DatasourceContext), symbol, start, end)

    def test_process_should_receive_dependencies_process_results_as_context(self):
        registration = mock()

        symbol = 'symbol'
        start = None
        end = None

        expected_a = pandas.DataFrame([1, 2, 3])
        expected_b = pandas.DataFrame([9, 8, 7])

        class DatasourceMock():

            def evaluate(self, context, s, ds, de):
                assert isinstance(context, task.DatasourceContext)
                deps = context.dependencies()
                assert isinstance(deps, dict)
                assert len(deps) is 2
                assert (deps['a'].values == expected_a.values).all()
                assert (deps['b'].values == expected_b.values).all()
                assert s == symbol
                assert ds == start
                assert de == end

        dependencies = {
            'a': mock(task.DataFrameDatasourceTask),
            'b': mock(task.DataFrameDatasourceTask),
        }
        when(dependencies['a']).process(symbol, start, end).thenReturn(expected_a)
        when(dependencies['b']).process(symbol, start, end).thenReturn(expected_b)

        task.DataFrameDatasourceTask(DatasourceMock(), registration, dependencies).process(symbol, start, end)


class TestDatasourceContext(unittest.TestCase):

    def test_dependencies_should_return_dependencies_given_through_constructor_when_no_reference_is_passed(self):
        expected = object()

        processingtask = task.DatasourceContext(expected)
        result = processingtask.dependencies()

        assert result is expected

    def test_dependencies_should_return_specific_dependency_when_reference_is_specifyed(self):
        deps = {
            'a': 0,
            'b': 1,
            'c': 2
        }

        processingtask = task.DatasourceContext(deps)
        result = processingtask.dependencies('b')

        assert result is 1

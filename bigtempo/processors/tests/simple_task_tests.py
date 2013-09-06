# -*- coding: utf-8 -*-


import unittest
from mockito import mock, when, any as anyx, verify

import bigtempo.processors.simple_task as task


class TestModuleFunctions(unittest.TestCase):

    def test_processingtask_factory_should_return_processing_task(self):
        instance = mock()
        registration = mock()
        dependencies = mock()

        result = task.factory(instance, registration, dependencies)
        assert isinstance(result, task.SimpleDatasourceTask)


class TestSimpleDatasourceTask(unittest.TestCase):

    def test_process_should_process_dependencies(self):
        instance = mock()
        registration = mock()
        dependencies = {
            'a': mock(task.SimpleDatasourceTask),
            'b': mock(task.SimpleDatasourceTask),
            'c': mock(task.SimpleDatasourceTask),
        }

        task.SimpleDatasourceTask(instance, registration, dependencies).process()

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
            'a': mock(task.SimpleDatasourceTask),
            'b': mock(task.SimpleDatasourceTask),
        }
        when(dependencies['a']).process().thenReturn('1')
        when(dependencies['b']).process().thenReturn('2')

        task.SimpleDatasourceTask(DatasourceMock(), mock(), dependencies).process()

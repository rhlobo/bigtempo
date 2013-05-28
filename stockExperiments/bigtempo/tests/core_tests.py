import unittest
from mockito import mock, when, any as anyx, verify

import bigtempo.core as core


class TestDatasourceEngine_for_datasources_without_dependencies(unittest.TestCase):

    def setUp(self):
        def builder(cls):
            return self.builder_mock.build(cls)
        self.builder_mock = mock()

        def processing_task_factory(instance, deps, lookback):
            return self.processing_task_factory_mock.create(instance)
        self.processing_task_factory_mock = mock()

        self.engine = core.DatasourceEngine(builder, processing_task_factory)

        class _Task(object):

            def __init__(self, instance):
                self.instance = instance

            def get_instance(self):
                return self.instance

        self.instances = []
        self.classes = []
        for i in range(3):
            @self.engine.datasource('REGISTERED_KEY_%i' % i)
            class _SampleDatasource(object):
                pass

            instance = _SampleDatasource()
            self.classes.append(_SampleDatasource)
            self.instances.append(instance)
            when(self.builder_mock).build(_SampleDatasource).thenReturn(instance)
            when(self.processing_task_factory_mock).create(instance).thenReturn(_Task(instance))

    def test_get_should_raise_error_when_reference_was_not_registered(self):
        self.assertRaises(KeyError, self.engine.get, 'NOT_REGISTERED_KEY')

    def test_get_should_not_raise_error_when_reference_was_registered(self):
        self.engine.get('REGISTERED_KEY_1')

    def test_get_should_not_use_builder_when_reference_was_not_registered(self):
        self.assertRaises(KeyError, self.engine.get, 'NOT_REGISTERED_KEY_1')
        verify(self.builder_mock, times=0).build(anyx())

    def test_get_should_use_builder_when_reference_was_registered(self):
        self.engine.get('REGISTERED_KEY_1')
        verify(self.builder_mock, times=1).build(anyx())

    def test_get_should_only_use_builder_once_for_a_registered_reference(self):
        for i in range(5):
            self.engine.get('REGISTERED_KEY_1')
        verify(self.builder_mock, times=1).build(anyx())

    def test_get_should_only_use_builder_once_for_each_registered_reference(self):
        for i in range(2):
            self.engine.get('REGISTERED_KEY_1')
        for i in range(2):
            self.engine.get('REGISTERED_KEY_2')
        self.engine.get('REGISTERED_KEY_1')
        verify(self.builder_mock, times=2).build(anyx())

    def test_get_should_use_processing_task_factory_in_each_call_for_registered_references(self):
        repetition = 3
        for i in range(repetition):
            self.engine.get('REGISTERED_KEY_1')
            self.engine.get('REGISTERED_KEY_2')
        verify(self.processing_task_factory_mock, times=repetition).create(self.instances[1])
        verify(self.processing_task_factory_mock, times=repetition).create(self.instances[2])


class TestDatasourceEngine_for_datasources_with_dependencies(unittest.TestCase):

    def setUp(self):
        def builder(cls):
            return self.builder_mock.build(cls)
        self.builder_mock = mock()

        def processing_task_factory(instance, deps, lookback):
            return self.processing_task_factory_mock.create(instance)
        self.processing_task_factory_mock = mock()

        self.engine = core.DatasourceEngine(builder, processing_task_factory)

        class _Task(object):

            def __init__(self, instance):
                self.instance = instance

            def get_instance(self):
                return self.instance

        self.classes = []
        self.instances = []
        registered_keys = []
        for i in range(3):
            @self.engine.datasource('REGISTERED_KEY_%i' % i, dependencies=list(registered_keys))
            class _SampleDatasource(object):
                pass

            instance = _SampleDatasource()
            self.classes.append(_SampleDatasource)
            self.instances.append(instance)
            registered_keys.append('REGISTERED_KEY_%i' % i)
            when(self.builder_mock).build(_SampleDatasource).thenReturn(instance)
            when(self.processing_task_factory_mock).create(instance).thenReturn(_Task(instance))

    def test_get_should_use_builder_for_required_reference_and_for_its_dependency(self):
        self.engine.get('REGISTERED_KEY_1')
        verify(self.builder_mock, times=1).build(self.classes[1])
        verify(self.builder_mock, times=1).build(self.classes[0])

    def test_get_should_use_builder_for_required_reference_and_for_each_dependency(self):
        self.engine.get('REGISTERED_KEY_2')
        verify(self.builder_mock, times=1).build(self.classes[2])
        verify(self.builder_mock, times=1).build(self.classes[1])
        verify(self.builder_mock, times=1).build(self.classes[0])

    def test_get_should_only_use_builder_once_for_each_reference_including_dependencies(self):
        for i in range(5):
            self.engine.get('REGISTERED_KEY_1')
        verify(self.builder_mock, times=1).build(self.classes[1])
        verify(self.builder_mock, times=1).build(self.classes[0])

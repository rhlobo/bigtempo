import unittest
from mockito import mock, when, any as anyx, verify

import bigtempo.core as core


class TestDatasourceEngine(unittest.TestCase):

    def setUp(self):
        self.builder_mock = mock()

        def builder(cls):
            return self.builder_mock.build(cls)

        self.engine = core.DatasourceEngine(builder)

        @self.engine.datasource('KEY')
        class SampleDatasource(object):
            pass

        when(self.builder_mock).build(anyx()).thenReturn(SampleDatasource())

    def test_get_should_raise_error_when_reference_was_not_registered(self):
        self.assertRaises(KeyError, self.engine.get, 'NOT_REGISTERED_KEY')

    def test_get_should_not_raise_error_when_reference_was_registered(self):
        self.engine.get('KEY')

    def test_get_should_not_use_builder_when_reference_was_not_registered(self):
        self.assertRaises(KeyError, self.engine.get, 'NOT_REGISTERED_KEY')
        verify(self.builder_mock, times=0).build(anyx())

    def test_get_should_use_builder_when_reference_was_registered(self):
        self.engine.get('KEY')
        verify(self.builder_mock, times=1).build(anyx())

    def test_get_should_only_use_builder_once_for_a_registered_reference(self):
        for i in range(5):
            self.engine.get('KEY')
        verify(self.builder_mock, times=1).build(anyx())

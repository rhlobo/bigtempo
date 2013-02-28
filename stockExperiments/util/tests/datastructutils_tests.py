import unittest
from mockito import mock, when, verify
import util.datastructutils as util


class TestLazyDict(unittest.TestCase):

    def test_keys_should_have_no_keys_just_after_initialized(self):
        ds = util.LazyDict(_MockFactory())
        assert len(ds.keys()) == 0

    def test_keys_should_return_keys_for_every_object_lazyloaded(self):
        key1 = "key1"
        key2 = "key2"
        factoryMock = mock()
        objectMock1 = mock()
        objectMock2 = mock()
        when(factoryMock).get().thenReturn(objectMock1).thenReturn(objectMock2).thenRaise(Exception('Out of mocks!'))
        ds = util.LazyDict(factoryMock)
        assert len(ds.keys()) == 0
        ds.get(key1)
        assert len(ds.keys()) == 1
        assert key1 in ds.keys()
        ds.get(key2)
        assert len(ds.keys()) == 2
        assert key1 in ds.keys()
        assert key2 in ds.keys()

    def test_get_should_lazyload_value_using_factory(self):
        key = "key"
        objectMock = mock()
        factoryMock = mock()
        when(factoryMock).get().thenReturn(objectMock)
        ds = util.LazyDict(factoryMock)
        assert ds.get(key) == objectMock
        verify(factoryMock, times=1).get()

    def test_get_should_store_lazyloaded_values(self):
        key = "key"
        objectMock = mock()
        factoryMock = mock()
        when(factoryMock).get().thenReturn(objectMock)
        ds = util.LazyDict(factoryMock)
        assert ds.get(key) == objectMock
        assert ds.get(key) == objectMock
        verify(factoryMock, times=1).get()

    def test_get_should_lazyload_value_for_each_key_only_once(self):
        key1 = "key1"
        key2 = "key2"
        factoryMock = mock()
        objectMock1 = mock()
        objectMock2 = mock()
        when(factoryMock).get().thenReturn(objectMock1).thenReturn(objectMock2).thenRaise(Exception('Out of mocks!'))
        ds = util.LazyDict(factoryMock)
        assert ds.get(key1) == objectMock1
        assert ds.get(key2) == objectMock2
        assert ds.get(key1) == objectMock1
        assert ds.get(key2) == objectMock2
        verify(factoryMock, times=2).get()

    def test_get_should_always_return_same_object_for_each_key(self):
        key1 = "key1"
        key2 = "key2"
        factoryMock = mock()
        objectMock1 = mock()
        objectMock2 = mock()
        when(factoryMock).get().thenReturn(objectMock1).thenReturn(objectMock2).thenRaise(Exception('Out of mocks!'))
        ds = util.LazyDict(factoryMock)
        assert ds.get(key1) == ds.get(key1)
        assert ds.get(key2) == ds.get(key2)


class TestListFactory(unittest.TestCase):

    def test_get_should_return_a_list(self):
        factory = util.ListFactory()
        result = factory.get()
        assert isinstance(result, list)

    def test_get_should_return_a_empty_list(self):
        factory = util.ListFactory()
        result = factory.get()
        assert len(result) == 0

    def test_get_should_always_return_a_new_list(self):
        factory = util.ListFactory()
        assert factory.get() == factory.get()
        assert factory.get() is not factory.get()


class TestDictFactory(unittest.TestCase):

    def test_get_should_return_a_list(self):
        factory = util.DictFactory()
        result = factory.get()
        assert isinstance(result, dict)

    def test_get_should_return_a_empty_list(self):
        factory = util.DictFactory()
        result = factory.get()
        assert len(result) == 0

    def test_get_should_always_return_a_new_list(self):
        factory = util.DictFactory()
        assert factory.get() == factory.get()
        assert factory.get() is not factory.get()


class _MockFactory(object):

    def get(self):
        raise NotImplementedError

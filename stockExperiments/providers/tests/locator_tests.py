import unittest
import providers.locator as locator
import providers.base as base


class TestLocator(unittest.TestCase):

    def test_should_have_get_method(self):
        locator.get()

    def test_locator_should_return_provider(self):
        provider = locator.get()
        assert isinstance(provider, base.Provider)

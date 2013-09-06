# -*- coding: utf-8 -*-


import unittest

import bigtempo.defaults as defaults


class TestModuleFunctions(unittest.TestCase):

    def test_builder_should_return_instance_of_given_class(self):
        class Foo(object):
            pass

        result = defaults.sample_datasource_factory(Foo)

        assert isinstance(result, Foo)

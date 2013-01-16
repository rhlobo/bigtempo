import unittest
import json
import ipyghstocks.options as options


class Test_AbstractHighChartsOptions(unittest.TestCase):

    def test_should_contain_method_that_returns_dict(self):
        abstractOptions = options._AbstractHighChartsOptions()
        abstractOptions.asDict()


class TestOptions(unittest.TestCase):

    def test_json_should_encode_json_without_errors(self):
        options.Options().json('container_id')

    def test_add_should_throw_value_error_if_given_object_is_not_AbstractHighChartsOptions(self):
        self.assertRaises(ValueError, options.Options().add, object())

    def test_add_should_throw_value_error_if_given_object_is_not_Axis_or_Series(self):
        self.assertRaises(ValueError, options.Options().add, _AbstractHighChartsOptions_Mock())

    def test_add_should_begin_without_axis_and_series(self):
        c_opts = options.Options()
        d_opts = json.loads(c_opts.json('container_id'))
        assert len(d_opts['yAxis']) == 0
        assert len(d_opts['series']) == 0

    def test_add_should_add_axis(self):
        name = 'test'
        c_opts = options.Options()
        c_opts.add(options.Axis(name))
        d_opts = json.loads(c_opts.json('container_id'))
        assert len(d_opts['yAxis']) == 1
        self.assertEqual(d_opts['yAxis'][0]['title']['text'], name)

    def test_add_should_add_series(self):
        name = 'test'
        c_opts = options.Options()
        c_opts.add(options.Series(name, []))
        d_opts = json.loads(c_opts.json('container_id'))
        assert len(d_opts['series']) == 1
        self.assertEqual(d_opts['series'][0]['name'], name)

    def test_add_should_add_two_axis(self):
        name1 = 'test1'
        name2 = 'test2'
        c_opts = options.Options()
        c_opts.add(options.Axis(name1))
        c_opts.add(options.Axis(name2))
        d_opts = json.loads(c_opts.json('container_id'))
        assert len(d_opts['yAxis']) == 2
        self.assertEqual(d_opts['yAxis'][0]['title']['text'], name1)
        self.assertEqual(d_opts['yAxis'][1]['title']['text'], name2)

    def test_add_should_add_two_series(self):
        name1 = 'test1'
        name2 = 'test2'
        c_opts = options.Options()
        c_opts.add(options.Series(name1, []))
        c_opts.add(options.Series(name2, []))
        d_opts = json.loads(c_opts.json('container_id'))
        assert len(d_opts['series']) == 2
        self.assertEqual(d_opts['series'][0]['name'], name1)
        self.assertEqual(d_opts['series'][1]['name'], name2)


class Test_AbstractHighChartsOptionsJSONEncoder(unittest.TestCase):

    def test_should_return_options_as_dict_when_Series(self):
        encoder = options._AbstractHighChartsOptionsJSONEncoder()
        assert isinstance(encoder.default(options.Series('test', [])), dict)

    def test_should_return_options_as_dict_when_Axis(self):
        encoder = options._AbstractHighChartsOptionsJSONEncoder()
        assert isinstance(encoder.default(options.Axis('test')), dict)

    def test_should_not_return_dict_when_not_AbstractHighChartsOptions(self):
        encoder = options._AbstractHighChartsOptionsJSONEncoder()
        assert not isinstance(encoder.default([]), dict)


class _AbstractHighChartsOptions_Mock(options._AbstractHighChartsOptions):
    pass

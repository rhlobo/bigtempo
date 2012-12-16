import unittest
from mockito import mock, when, verify, unstub, any as anyv
import re
import ipyghstocks.chart as chart


class TestPlot(unittest.TestCase):

    def test_plot_should_importlibs_generate_id_once_and_use_it_on_rest(self):
        container_id = 'random'

        options = mock(chart.options.Options)
        when(options).json().thenReturn('')
        when(chart)._generate_id().thenReturn(container_id)
        when(chart)._generate_container_html(container_id).thenReturn('')
        when(chart)._generate_javascript(container_id, anyv()).thenReturn('')

        chart.plot(options)
        verify(chart, times=1)._generate_id()
        verify(chart, times=1)._generate_container_html(container_id)
        verify(chart, times=1)._generate_javascript(container_id, anyv())
        unstub()


class TestIpyghstocksChartModuleGenerateIdFunction(unittest.TestCase):

    def __init__(self, a):
        unittest.TestCase.__init__(self, a)
        self.testloops = 100

    def test_generate_id_function_should_always_return_different_ids(self):
        ids = {}
        for i in range(self.testloops):
            generated = chart._generate_id()
            assert ids.get(generated) is None
            ids[generated] = generated

    def test_generate_id_function_should_always_starts_with_alpha(self):
        for i in range(self.testloops):
            generated = chart._generate_id()
            assert generated[0].isalpha()

    def test_generate_id_function_should_be_long_enough(self):
        for i in range(self.testloops):
            generated = chart._generate_id()
            assert len(generated) > 10

    def test_generate_id_function_should_not_have_whitespaces(self):
        regex = re.compile(r'\s+')
        for i in range(self.testloops):
            generated = chart._generate_id()
            assert regex.search(generated) is None


class TestIpyghstocksChartModuleGenerateHtmlFunction(unittest.TestCase):

    def __init__(self, a):
        unittest.TestCase.__init__(self, a)
        self.regex = re.compile(r'<div\s+id="(.*?)"\s+.*?/>', re.IGNORECASE)

    def test_generate_container_html_should_return_div_tag(self):
        generated = chart._generate_container_html('')
        result = self.regex.search(generated)
        assert result is not None

    def test_generate_container_html_returned_tag_should_have_given_id(self):
        container_id = "container_id"
        generated = chart._generate_container_html(container_id)
        result = self.regex.search(generated)
        if result is not None:
            assert result.group(1) == container_id


class TestIpyghstocksChartModuleGenerateJavascriptFunction(unittest.TestCase):

    def test_generate_javascript_should_return_script_tag(self):
        regex = re.compile(r'.*?<script>.*?</script>.*?', re.I | re.M | re.S)
        generated = chart._generate_javascript('', '')
        result = regex.search(generated)
        assert result is not None

    def test_generate_javascript_returned_script_should_have_js_function(self):
        container_id = "container_id"
        regex_str = (
                     r'\s*<script>.*?\s+function draw' +
                     container_id +
                     r'\(\) \{.*?\}.*?</script>\s*'
                    )
        regex = re.compile(regex_str, re.I | re.M | re.S)
        generated = chart._generate_javascript(container_id, '')
        result = regex.search(generated)
        assert result is not None


class TestIpyghstocksChartModuleImportLibsFunction(unittest.TestCase):

    def test_import_libs_should_return_script_tag(self):
        regex = re.compile(r'.*?<script>.*?</script>.*?', re.I | re.M | re.S)
        generated = chart._importLibs('')
        result = regex.search(generated)
        assert result is not None

    def test_import_libs_returned_script_should_have_js_function_call(self):
        container_id = "container_id"
        regex_str = (
                     r'\s*<script>.*?\s+draw' +
                     container_id +
                     r'\(\);.*?</script>\s*'
                    )
        regex = re.compile(regex_str, re.I | re.M | re.S)
        generated = chart._importLibs(container_id)
        result = regex.search(generated)
        assert result is not None

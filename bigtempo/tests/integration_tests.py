# -*- coding: utf-8 -*-


import unittest

import bigtempo.core as core


class TestIntegration_TagSelector_use_cases(unittest.TestCase):

    def setUp(self):
        self.engine = core.DatasourceEngine()
        _create_test_scenario(self.engine)

    def test_select_with_no_selector_results_empty_selection(self):
        selection = self.engine.select()
        assert len(selection) is 0

    def test_select_with_unknown_selector_results_empty_selection(self):
        selection = self.engine.select('UNKNOWN_TAG_OR_REFERENCE')
        assert len(selection) is 0

    def test_select_with_known_reference_results_in_existing_reference(self):
        selection = self.engine.select('RAW_QUOTE_01')
        assert len(selection) is 1
        assert selection.get(0).process('SYMBOL') == 'RAW_QUOTE_01_RESULT_FOR_SYMBOL'

        selection = self.engine.select('RAW_QUOTE_02')
        assert len(selection) is 1
        assert selection.get(0).process('SYMBOL') == 'RAW_QUOTE_02_RESULT_FOR_SYMBOL'

    def test_select_with_known_tag_results_in_existing_references(self):
        selection = self.engine.select('RAW_QUOTE')
        assert len(selection) is 2

        result = selection.get()
        for reference, process_result in [('RAW_QUOTE_01', 'RAW_QUOTE_01_RESULT_FOR_SYMBOL'),
                                          ('RAW_QUOTE_02', 'RAW_QUOTE_02_RESULT_FOR_SYMBOL')]:
            assert reference in result.keys()
            assert result[reference].process('SYMBOL') == process_result

    def test_select_with_multiple_known_tags_results_in_existing_references(self):
        selection = self.engine.select('RAW_QUOTE').difference('RAW_QUOTE_02').union('YA_RAW_QUOTE')
        assert len(selection) is 2

        result = selection.get()
        for reference, process_result in [('RAW_QUOTE_01', 'RAW_QUOTE_01_RESULT_FOR_SYMBOL'),
                                          ('YET_ANOTHER_RAW_QUOTE', 'YET_ANOTHER_RAW_QUOTE_02_RESULT_FOR_SYMBOL')]:
            assert reference in result.keys()
            assert result[reference].process('SYMBOL') == process_result

    def test_select_should_return_existing_references_that_have_given_tag_but_dont_have_other(self):
        selection = self.engine.select('RAW_QUOTE').difference('NOT_TRUSTABLE_SOURCE')
        assert len(selection) is 1
        assert selection.get(0).process('SYMBOL') == 'RAW_QUOTE_02_RESULT_FOR_SYMBOL'

    def test_select_should_return_existing_references_that_have_given_tag_combination(self):
        selection = self.engine.select('RAW_QUOTE', 'NOT_TRUSTABLE_SOURCE')
        assert len(selection) is 1
        assert selection.get(0).process('SYMBOL') == 'RAW_QUOTE_01_RESULT_FOR_SYMBOL'

    def test_select_should_return_existing_reference_based_on_certain_reference(self):
        selection = self.engine.select('BYPRODUCT', '{RAW_QUOTE_01}')
        assert len(selection) is 1
        assert selection.get(0).process('SYMBOL') == 'FOREACH_BYPRODUCT_01:RAW_QUOTE_01_RESULT_FOR_SYMBOL'

    def test_select_should_return_existing_point_reference_based_on_certain_reference(self):
        selection = self.engine.select('POINT', '{RAW_QUOTE_01}')
        assert len(selection) is 1
        assert selection.get(0).process('SYMBOL') == 'POINT:(RAW_QUOTE_01,FOREACH_BYPRODUCT_01:RAW_QUOTE_01)_RESULT_FOR_SYMBOL'

    def test_select_should_return_existing_point_reference_not_based_on_certain_reference(self):
        selection = self.engine.select('POINT').difference('{NOT_TRUSTABLE_SOURCE}')
        assert len(selection) is 4

    def test_select_should_return_every_reference_that_is_based_on_given_reference(self):
        selection = self.engine.select('{RAW_QUOTE_01}')
        assert len(selection) is 2
        for reference in selection:
            assert reference in ['FOREACH_BYPRODUCT_01:RAW_QUOTE_01', 'POINT:(RAW_QUOTE_01,FOREACH_BYPRODUCT_01:RAW_QUOTE_01)']

    def test_tags_should_return_every_tag_for_given_reference(self):
        selection = self.engine.tags('POINT:(RAW_QUOTE_01,FOREACH_BYPRODUCT_01:RAW_QUOTE_01)')
        assert len(selection) is 8
        for reference in selection:
            assert reference in ["{NOT_TRUSTABLE_SOURCE}",
                                 "POINT",
                                 "{RAW_QUOTE_01}",
                                 "POINT:(RAW_QUOTE_01,FOREACH_BYPRODUCT_01:RAW_QUOTE_01)",
                                 "{INDICATOR}",
                                 "{FOREACH_BYPRODUCT_01:RAW_QUOTE_01}",
                                 "{BYPRODUCT}",
                                 "{RAW_QUOTE}"]


def _create_test_scenario(engine):

    @engine.datasource('RAW_QUOTE_01',
                       tags=['RAW_QUOTE', 'NOT_TRUSTABLE_SOURCE'])
    class RawQuote01(object):

        def evaluate(self, context, symbol, start=None, end=None):
            return 'RAW_QUOTE_01_RESULT_FOR_%s' % symbol

    @engine.for_synched(engine.select('RAW_QUOTE').union('YA_RAW_QUOTE').union('QUOTE'), engine.select('BYPRODUCT'))
    def _datasource_factory1(raw_reference, byproduct_reference):
        dsname = 'POINT:(%s,%s)' % (raw_reference, byproduct_reference)

        @engine.datasource(dsname,
                           dependencies=[byproduct_reference],
                           tags=['POINT'])
        class Point(object):

            def evaluate(self, context, symbol, start=None, end=None):
                return '%s_RESULT_FOR_%s' % (dsname, symbol)

    @engine.for_each(engine.select('RAW_QUOTE'))
    def _datasource_factory2(raw_reference):
        dsname = 'FOREACH_BYPRODUCT_01:%s' % raw_reference

        @engine.datasource(dsname,
                           dependencies=[raw_reference],
                           tags=['BYPRODUCT', 'INDICATOR'])
        class ByProduct01(object):

            def evaluate(self, context, symbol, start=None, end=None):
                return '%s_RESULT_FOR_%s' % (dsname, symbol)

    @engine.datasource('RAW_QUOTE_02',
                       tags=['RAW_QUOTE'])
    class RawQuote02(object):

        def evaluate(self, context, symbol, start=None, end=None):
            return 'RAW_QUOTE_02_RESULT_FOR_%s' % symbol

    @engine.datasource('YET_ANOTHER_RAW_QUOTE',
                       tags=['YA_RAW_QUOTE', 'NOT_TRUSTABLE_SOURCE'])
    class RawQuote03(object):

        def evaluate(self, context, symbol, start=None, end=None):
            return 'YET_ANOTHER_RAW_QUOTE_02_RESULT_FOR_%s' % symbol

    @engine.datasource('YET_ANOTHER_RAW_QUOTE_BYPRODUCT',
                       dependencies=['YET_ANOTHER_RAW_QUOTE'],
                       tags=['BYPRODUCT'])
    class ByProduct03(object):

        def evaluate(self, context, symbol, start=None, end=None):
            return 'YET_ANOTHER_RAW_QUOTE_RESULT_FOR_%s' % (symbol)

    for i in range(3):
        @engine.datasource('QUOTE_0%i' % i,
                           tags=['QUOTE'])
        class Quote(object):

            def evaluate(self, context, symbol, start=None, end=None):
                return 'QUOTE_0%i_RESULT_FOR_%s' % (i, symbol)

    @engine.for_each(engine.select('QUOTE'))
    def _datasource_factory3(raw_reference):
        dsname = 'BYPRODUCT_02:%s' % raw_reference

        @engine.datasource(dsname,
                           dependencies=[raw_reference],
                           tags=['BYPRODUCT'])
        class ByProduct02(object):

            def evaluate(self, context, symbol, start=None, end=None):
                return '%s_RESULT_FOR_%s' % (dsname, symbol)

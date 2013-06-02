import unittest
from mockito import mock, when, any as anyx, verify, verifyNoMoreInteractions
import collections as collections

import util.testutils as testutils
import bigtempo.tagselection as tagselection


class TestTagSelection(unittest.TestCase):

    def setUp(self):
        self.callable_factory = mock()
        self.tag_mappings = collections.defaultdict(set)
        self.tagSelection = tagselection._TagSelection(self.tag_mappings, testutils.CallableMock(self.callable_factory))

    def test__evaluate_selectors_should_return_entire_set_of_references_when_only_one_tag_is_passed(self):
        selection = self.tagSelection
        self.tag_mappings.update({
                                 'A': set('abcdef'),
                                 'B': set('bcde'),
                                 'C': set('cd')
                                 })

        result = selection._evaluate_selectors('A')
        assert len(result) is 6
        for c in 'abcdef':
            assert c in result

    def test__evaluate_selectors_should_return_intersection_of_references_when_multiple_tags_are_passed(self):
        selection = self.tagSelection
        self.tag_mappings.update({
                                 'A': set('abcdef'),
                                 'B': set('bcde'),
                                 'C': set('xcd14')
                                 })

        result = selection._evaluate_selectors('A', 'B')
        assert len(result) is 4
        for c in 'bcde':
            assert c in result

        result = selection._evaluate_selectors('A', 'C')
        assert len(result) is 2
        for c in 'cd':
            assert c in result

        result = selection._evaluate_selectors('A', 'B', 'C')
        assert len(result) is 2
        for c in 'cd':
            assert c in result

    def test__evaluate_selectors_return_should_not_depend_on_selector_order(self):
        selection = self.tagSelection
        self.tag_mappings.update({
                                 'A': set('abcdef'),
                                 'B': set('bcde zxw'),
                                 })

        assert selection._evaluate_selectors('A', 'B') == selection._evaluate_selectors('B', 'A')

    def test_get_should_return_empty_dictiornary_when_nothing_was_selected(self):
        result = self.tagSelection.get()
        assert isinstance(result, dict)
        assert len(result) is 0

    def test_get_should_return_populted_dictiornary_when_something_was_selected(self):
        self.tag_mappings.update({
                                 'A': set(['a1', 'a2', 'a3'])
                                 })
        when(self.callable_factory).__call__('a1').thenReturn('a1')
        when(self.callable_factory).__call__('a2').thenReturn('a2')
        when(self.callable_factory).__call__('a3').thenReturn('a3')

        result = self.tagSelection.union('A').get()

        assert isinstance(result, dict)
        assert len(result) == 3

    def test_get_should_return_populted_dictiornary_when_something_was_selected(self):
        self.tag_mappings.update({
                                 'A': set(['a1', 'a2', 'a3'])
                                 })
        when(self.callable_factory).__call__('a1').thenReturn('a1')
        when(self.callable_factory).__call__('a2').thenReturn('a2')
        when(self.callable_factory).__call__('a3').thenReturn('a3')

        result = self.tagSelection.union('A').get()

        assert isinstance(result, dict)
        assert len(result) is 3
        assert 'a1' in result
        assert 'a2' in result
        assert 'a3' in result

    def test_get_should_use_callableFactory_to_populte_resultant_dictiornary(self):
        self.tag_mappings.update({
                                 'A': set(['a1', 'a2', 'a3'])
                                 })
        when(self.callable_factory).__call__('a1').thenReturn('a1')
        when(self.callable_factory).__call__('a2').thenReturn('a2')
        when(self.callable_factory).__call__('a3').thenReturn('a3')

        self.tagSelection.union('A').get()

        verify(self.callable_factory, times=1).__call__('a1')
        verify(self.callable_factory, times=1).__call__('a2')
        verify(self.callable_factory, times=1).__call__('a3')
        verifyNoMoreInteractions(self.callable_factory)

    def test_initial_selection_should_be_empty(self):
        assert len(self.tagSelection.selection) is 0

    def test_all_should_select_every_reference_available(self):
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.all().selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_union_should_select_references_for_given_tag(self):
        self.tagSelection.selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.union('2').selection
        assert len(result) is 7
        for c in 'qwe defg':
            assert c in result

    def test_union_should_select_references_for_intersection_of_given_tags(self):
        self.tagSelection.selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.union('1', '2').selection
        assert len(result) is 6
        for c in 'qwe xd':
            assert c in result

    def test_union_should_not_change_selection_when_no_tags_are_given(self):
        self.tagSelection.selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.union().selection
        assert len(result) is 4
        for c in 'qwe ':
            assert c in result

    def test_union_should_not_change_selection_when_non_registered_tags_are_given(self):
        self.tagSelection.selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.union('X').selection
        assert len(result) is 4
        for c in 'qwe ':
            assert c in result

    def test_intersection_should_filter_selection_with_references_for_given_tag(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.intersection('2').selection
        assert len(result) is 4
        for c in 'defg':
            assert c in result

    def test_intersection_should_filter_selection_with_references_for_intersection_of_given_tags(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.intersection('1', '2').selection
        assert len(result) is 1
        for c in 'd':
            assert c in result

    def test_intersection_should_filter_selection_when_no_tags_are_given(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.intersection().selection
        assert len(result) is 0

    def test_intersection_should_empty_out_selection_when_non_registered_tag_is_given(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.intersection('X').selection
        assert len(result) is 0

    def test_difference_should_subtract_from_selection_with_references_for_given_tag(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.difference('2').selection
        assert len(result) is 6
        for c in 'abchij':
            assert c in result

    def test_difference_should_subtract_from_selection_with_references_of_intersection_of_given_tags(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.difference('1', '2').selection
        assert len(result) is 9
        for c in 'abcefghij':
            assert c in result

    def test_difference_should_not_subtract_from_selection_when_no_tags_are_given(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.difference().selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_difference_should_not_subtract_from_selection_when_non_registered_tag_is_given(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.difference('X').selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_symmetric_difference_for_given_tag(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference('2').selection
        assert len(result) is 7
        for c in 'xabchij':
            assert c in result

    def test_symmetric_difference_using_intersection_of_given_tags(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference('1', '2').selection
        assert len(result) is 10
        for c in 'xabcefghij':
            assert c in result

    def test_symmetric_difference_should_not_change_selection_when_no_tags_are_given(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference().selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_symmetric_difference_should_not_change_selection_when_non_registered_tag_is_given(self):
        self.tagSelection.selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference('X').selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result


class TestTagSelector(unittest.TestCase):

    def setUp(self):
        self.TagSelection = tagselection._TagSelection

    def tearDown(self):
        tagselection._TagSelection = self.TagSelection

    def test_get_should_return_tag_selection(self):
        result = tagselection.TagSelector(None).get()
        assert isinstance(result, tagselection._TagSelection)

    def test_get_should_instantiate_new_tag_selection_and_initiate_it(self):
        callable_factory = mock()
        args = ['selector']

        tagSelectionMock = mock(tagselection._TagSelection)
        when(tagSelectionMock).__call__(anyx(), anyx()).thenReturn(tagSelectionMock)
        tagselection._TagSelection = testutils.CallableMock(tagSelectionMock)

        tagselection.TagSelector(callable_factory).get(*args)
        verify(tagSelectionMock, times=1).__call__(anyx(collections.defaultdict), callable_factory)
        verify(tagSelectionMock, times=1).union(*args)

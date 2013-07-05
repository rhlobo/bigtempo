import unittest
from mockito import mock, when, any as anyx, verify, verifyNoMoreInteractions
import collections as collections

import util.testutils as testutils
import bigtempo.tagselection as tagselection


class TestTagRegistrationManager_registrations(unittest.TestCase):

    def setUp(self):
        self.registrations = {}
        self.manager = tagselection.TagRegistrationManager(self.registrations)
        self.listener_mock = mock()
        self.listener_callable_mock = testutils.CallableMock(self.listener_mock)

    def test_register_should_not_call_listener_when_there_is_no_existent_reference(self):
        selection = []

        self.manager.register(self.listener_callable_mock, selection)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_should_call_listener_for_existent_reference_when_there_is_one_selector(self):
        reference = 'REFERENCE'
        selection = [reference]

        self.manager.register(self.listener_callable_mock, selection)
        verify(self.listener_mock, times=1).__call__(reference)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_should_call_listener_for_each_existent_reference_when_there_is_one_selector(self):
        reference1 = 'REFERENCE1'
        reference2 = 'REFERENCE2'
        selection = [reference1, reference2]

        self.manager.register(self.listener_callable_mock, selection)
        verify(self.listener_mock, times=1).__call__(reference1)
        verify(self.listener_mock, times=1).__call__(reference2)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_should_call_listener_for_each_existent_combination_of_references_when_there_are_multiple_selectors(self):
        reference1a = 'REFERENCE1a'
        reference2a = 'REFERENCE2a'
        selection_a = [reference1a, reference2a]

        reference1b = 'REFERENCE1b'
        reference2b = 'REFERENCE2b'
        selection_b = [reference1b, reference2b]

        self.manager.register(self.listener_callable_mock, selection_a, selection_b)
        verify(self.listener_mock, times=1).__call__(reference1a, reference1b)
        verify(self.listener_mock, times=1).__call__(reference1a, reference2b)
        verify(self.listener_mock, times=1).__call__(reference2a, reference1b)
        verify(self.listener_mock, times=1).__call__(reference2a, reference2b)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_should_call_listener_for_late_reference_when_there_is_one_selector(self):
        reference = 'REFERENCE'

        selection = mock()
        when(selection).__iter__().thenReturn([].__iter__()).thenReturn([reference].__iter__())
        when(selection).is_elegible(reference).thenReturn(True)

        self.manager.register(self.listener_callable_mock, testutils.IterableMock(selection))
        verify(self.listener_mock, times=0).__call__(anyx())
        verifyNoMoreInteractions(self.listener_mock)

        self.manager.evaluate_new_candidate(reference)
        verify(self.listener_mock, times=1).__call__(reference)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_should_call_listener_for_each_late_reference_when_there_is_one_selector(self):
        reference1 = 'REFERENCE1'
        reference2 = 'REFERENCE2'
        reference3 = 'REFERENCE3'

        selection = mock()
        (when(selection).__iter__().thenReturn([reference1].__iter__())
            .thenReturn([reference1, reference2].__iter__())
            .thenReturn([reference1, reference2, reference3].__iter__()))
        when(selection).is_elegible(reference2).thenReturn(True)
        when(selection).is_elegible(reference3).thenReturn(True)

        self.manager.register(self.listener_callable_mock, testutils.IterableMock(selection))
        verify(self.listener_mock, times=1).__call__(reference1)
        verifyNoMoreInteractions(self.listener_mock)

        self.manager.evaluate_new_candidate(reference2)
        verify(self.listener_mock, times=1).__call__(reference2)
        verifyNoMoreInteractions(self.listener_mock)

        self.manager.evaluate_new_candidate(reference3)
        verify(self.listener_mock, times=1).__call__(reference3)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_should_call_listener_for_each_late_combination_of_references_when_there_are_multiple_selectors(self):
        reference1a = 'REFERENCE1a'
        reference2a = 'REFERENCE2a'
        reference1b = 'REFERENCE1b'
        reference2b = 'REFERENCE2b'

        selection_a = mock()
        (when(selection_a).__iter__()
            .thenReturn([reference1a].__iter__())
            .thenReturn([reference1a, reference2a].__iter__())
            .thenReturn([reference1a, reference2a].__iter__()))
        when(selection_a).is_elegible(reference2a).thenReturn(True)

        selection_b = mock()
        (when(selection_b).__iter__()
            .thenReturn([reference1b].__iter__())
            .thenReturn([reference1b].__iter__())
            .thenReturn([reference1b, reference2b].__iter__()))
        when(selection_b).is_elegible(reference2b).thenReturn(True)

        self.manager.register(self.listener_callable_mock, testutils.IterableMock(selection_a), testutils.IterableMock(selection_b))
        verify(self.listener_mock, times=1).__call__(reference1a, reference1b)
        verifyNoMoreInteractions(self.listener_mock)

        self.manager.evaluate_new_candidate(reference2a)
        verify(self.listener_mock, times=1).__call__(reference2a, reference1b)
        verifyNoMoreInteractions(self.listener_mock)

        self.manager.evaluate_new_candidate(reference2b)
        verify(self.listener_mock, times=1).__call__(reference1a, reference2b)
        verify(self.listener_mock, times=1).__call__(reference2a, reference2b)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_synched_should_not_call_listener_when_there_is_no_existent_reference(self):
        selection = [[]]

        self.manager.register_synched(self.listener_callable_mock, selection)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_synched_should_call_listener_for_existent_reference_when_there_is_one_selector(self):
        reference = 'REFERENCE'
        selection = [[reference]]

        self.manager.register_synched(self.listener_callable_mock, selection)
        verify(self.listener_mock, times=1).__call__(reference)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_synched_should_call_listener_for_each_existent_reference_when_there_is_one_selector(self):
        reference1 = 'REFERENCE1'
        reference2 = 'REFERENCE2'
        selection = [[reference1, reference2]]

        self.manager.register_synched(self.listener_callable_mock, selection)
        verify(self.listener_mock, times=1).__call__(reference1)
        verify(self.listener_mock, times=1).__call__(reference2)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_synched_should_call_listener_for_each_existent_combination_of_references_when_there_are_multiple_selectors(self):
        reference1a = 'X1'
        reference2a = 'X2'
        reference3a = 'X3'
        selection_a = [reference1a, reference2a, reference3a]

        reference1b = 'R1'
        reference2b = 'R2'
        reference3b = 'R3'

        selection_b = mock()
        (when(selection_b).__iter__()
            .thenReturn([reference1b, reference2b, reference3b].__iter__()))
        when(selection_b).intersection('{%s}' % reference1a).thenReturn([reference1b])
        when(selection_b).intersection('{%s}' % reference2a).thenReturn([reference2b])
        when(selection_b).intersection('{%s}' % reference3a).thenReturn([reference3b])

        self.manager.register_synched(self.listener_callable_mock,
                              [selection_a, testutils.IterableMock(selection_b)])
        verify(self.listener_mock, times=1).__call__(reference1a, reference1b)
        verify(self.listener_mock, times=1).__call__(reference2a, reference2b)
        verify(self.listener_mock, times=1).__call__(reference3a, reference3b)
        verifyNoMoreInteractions(self.listener_mock)

    def test_register_synched_should_call_listener_for_late_reference_when_there_is_one_selector(self):
        reference = 'REFERENCE'

        selection = mock()
        when(selection).__iter__().thenReturn([].__iter__()).thenReturn([reference].__iter__())
        when(selection).is_elegible(reference).thenReturn(True)

        self.manager.register_synched(self.listener_callable_mock, [testutils.IterableMock(selection)])
        verify(self.listener_mock, times=0).__call__(anyx())
        verifyNoMoreInteractions(self.listener_mock)

        self.manager.evaluate_new_candidate(reference)
        verify(self.listener_mock, times=1).__call__(reference)
        verifyNoMoreInteractions(self.listener_mock)


class TestTagRegistrationManager_tag_inference(unittest.TestCase):

    def setUp(self):
        self.registrations = {}
        self.manager = tagselection.TagRegistrationManager(self.registrations)

    def test_infere_tags_should_infere_tag_using_reference_name(self):
        reference = 'REFERENCE'

        result = self.manager.infere_tags(reference)

        assert isinstance(result, set)
        assert len(result) is 1
        assert reference in result

    def test_infere_tags_should_infere_tags_using_reference_depencies(self):
        reference = 'REFERENCE'
        expected = ['{D1}', '{D2}', '{D3}', 'REFERENCE']

        self.registrations.update({
            reference: {'dependencies': set(['D1', 'D2', 'D3'])}
        })

        _process_dependencies(self, ['D3', 'D2', 'D1'])
        result = self.manager.infere_tags(reference)

        assert isinstance(result, set)
        assert len(result) is len(expected)
        for tag in expected:
            assert tag in result

    def test_infere_tags_should_infere_tags_using_reference_depencies_recursively(self):
        reference = 'REFERENCE'
        expected = ['{D1}', '{D2}', '{D3}', 'REFERENCE',
                    '{SDA1}', '{SDA2}',
                    '{SDC1}', '{SDC2}',
                    '{SDC1}', '{SDC2}',
                    '{X1}', '{X2}']

        self.registrations.update({
            reference: {'dependencies': set(['D1', 'D2', 'D3'])},
            'D1': {'dependencies': set(['SDA1', 'SDA2'])},
            'D2': {'dependencies': set(['SDB1', 'SDB2'])},
            'D3': {'dependencies': set(['SDC1', 'SDC2'])},
            'SDA1': {'dependencies': set(['X1', 'X2'])}
        })

        _process_dependencies(self, ['X2', 'X1', 'SDC2', 'SDC1', 'SDB2', 'SDB1', 'SDA2', 'SDA1', 'D3', 'D2', 'D1'])
        result = self.manager.infere_tags(reference)

        assert isinstance(result, set)
        assert len(result) is len(expected)
        for tag in expected:
            assert tag in result

    def test_infere_tags_should_infere_tags_using_reference_depencies_tags(self):
        reference = 'REFERENCE'
        expected = ['REFERENCE',
                    '{D1}', '{TD1A}', '{TD1B}',
                    '{D2}', '{TD2A}', '{TD2B}']

        self.registrations.update({
            reference: {
                'dependencies': set(['D1', 'D2'])
            },
            'D1': {
                'dependencies': set(),
                'tags': set(['TD1A', 'TD1B'])
            },
            'D2': {
                'dependencies': set(),
                'tags': set(['TD2A', 'TD2B'])
            }
        })

        _process_dependencies(self, ['D2', 'D1'])
        result = self.manager.infere_tags(reference)

        assert isinstance(result, set)
        assert len(result) is len(expected)
        for tag in expected:
            assert tag in result

    def test_infere_tags_should_infere_tags_using_reference_depencies_tags_recursively(self):
        reference = 'REFERENCE'
        expected = ['REFERENCE',
                    '{D1}', '{TD1A}', '{TD1B}',
                    '{D2}', '{TD2A}', '{TD2B}',
                    '{D3}', '{TD3A}', '{TD3B}',
                    '{X1}', '{TX1A}', '{TX1B}',
                    '{X2}', '{TX2A}', '{TX2B}',
                    '{X3}', '{TX3A}', '{TX3B}']

        self.registrations.update({
            reference: {'dependencies': set(['D1', 'D2', 'D3'])},
            'D1': {
                'dependencies': set(['X1']),
                'tags': set(['TD1A', 'TD1B'])
            },
            'D2': {
                'dependencies': set(['X2']),
                'tags': set(['TD2A', 'TD2B'])
            },
            'D3': {
                'dependencies': set(['X3']),
                'tags': set(['TD3A', 'TD3B'])
            },
            'X1': {
                'dependencies': set(),
                'tags': set(['TX1A', 'TX1B'])
            },
            'X2': {
                'dependencies': set(),
                'tags': set(['TX2A', 'TX2B'])
            },
            'X3': {
                'dependencies': set(),
                'tags': set(['TX3A', 'TX3B'])
            }
        })

        _process_dependencies(self, ['X3', 'X2', 'X1', 'D3', 'D2', 'D1'])
        result = self.manager.infere_tags(reference)

        assert isinstance(result, set)
        assert len(result) is len(expected)
        for tag in expected:
            assert tag in result


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

    def test_get_should_return_dictiornary_with_correct_data_when_something_was_selected(self):
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
        assert len(self.tagSelection._selection) is 0

    def test_all_should_select_every_reference_available(self):
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.all()._selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_union_should_select_references_for_given_tag(self):
        self.tagSelection._initial_selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.union('2')._selection
        assert len(result) is 7
        for c in 'qwe defg':
            assert c in result

    def test_union_should_select_references_for_intersection_of_given_tags(self):
        self.tagSelection._initial_selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.union('1', '2')._selection
        assert len(result) is 6
        for c in 'qwe xd':
            assert c in result

    def test_union_should_not_change_selection_when_no_tags_are_given(self):
        self.tagSelection._initial_selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.union()._selection
        assert len(result) is 4
        for c in 'qwe ':
            assert c in result

    def test_union_should_not_change_selection_when_non_registered_tags_are_given(self):
        self.tagSelection._initial_selection = set('qwe ')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.union('X')._selection
        assert len(result) is 4
        for c in 'qwe ':
            assert c in result

    def test_intersection_should_filter_selection_with_references_for_given_tag(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.intersection('2')._selection
        assert len(result) is 4
        for c in 'defg':
            assert c in result

    def test_intersection_should_filter_selection_with_references_for_intersection_of_given_tags(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.intersection('1', '2')._selection
        assert len(result) is 1
        for c in 'd':
            assert c in result

    def test_intersection_should_filter_selection_when_no_tags_are_given(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.intersection()._selection
        assert len(result) is 0

    def test_intersection_should_empty_out_selection_when_non_registered_tag_is_given(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.intersection('X')._selection
        assert len(result) is 0

    def test_difference_should_subtract_from_selection_with_references_for_given_tag(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        result = self.tagSelection.difference('2')._selection
        assert len(result) is 6
        for c in 'abchij':
            assert c in result

    def test_difference_should_subtract_from_selection_with_references_of_intersection_of_given_tags(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.difference('1', '2')._selection
        assert len(result) is 9
        for c in 'abcefghij':
            assert c in result

    def test_difference_should_not_subtract_from_selection_when_no_tags_are_given(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.difference()._selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_difference_should_not_subtract_from_selection_when_non_registered_tag_is_given(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.difference('X')._selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_symmetric_difference_for_given_tag(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference('2')._selection
        assert len(result) is 7
        for c in 'xabchij':
            assert c in result

    def test_symmetric_difference_using_intersection_of_given_tags(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference('1', '2')._selection
        assert len(result) is 10
        for c in 'xabcefghij':
            assert c in result

    def test_symmetric_difference_should_not_change_selection_when_no_tags_are_given(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference()._selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_symmetric_difference_should_not_change_selection_when_non_registered_tag_is_given(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('xabcd'),
                                 '2': set('xdefg'),
                                 '3': set('xghij')
                                 })
        result = self.tagSelection.symmetric_difference('X')._selection
        assert len(result) is 10
        for c in 'abcdefghij':
            assert c in result

    def test_selection_iterator(self):
        self.tagSelection._initial_selection = set('abcdefghij')

        iterated = set()
        for item in self.tagSelection:
            assert item not in iterated
            iterated.add(item)

        assert len(iterated) is 10

    def test_selection_iterator_with_operations(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })

        selection = self.tagSelection.intersection('2')

        iterated = set()
        for item in selection:
            assert item not in iterated
            iterated.add(item)

        for c in 'defg':
            assert c in iterated

        assert len(iterated) is 4

    def test_selection_length(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        assert len(self.tagSelection) is 10

    def test_selection_length_with_operations(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })

        selection = self.tagSelection.intersection('2')
        assert len(selection) is 4

    def test_is_elegible(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })
        selection = self.tagSelection.intersection('2')

        for c in 'defg':
            assert selection.is_elegible(c)

        for c in 'abchij':
            assert not selection.is_elegible(c)

    def test_operation_returns_new_instance(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({
                                 '1': set('abcd'),
                                 '2': set('defg'),
                                 '3': set('ghij')
                                 })

        selection = self.tagSelection.intersection('2')
        assert not selection in self.tagSelection

    def test_instance_is_not_changed_upon_operation_being_able_to_be_execute_multiple_times(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({'2': set('defg')})

        self.tagSelection.union('2')
        self.tagSelection.symmetric_difference('2')
        self.tagSelection.intersection('2')
        self.tagSelection.difference('2')
        assert len(self.tagSelection) is 10

    def test_get_without_passing_index_should_return_dict_with_each_item_result_from_callable(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({'2': set('defg')})

        result = self.tagSelection.difference('2').get()
        assert isinstance(result, dict)
        assert len(result) is 6

        verify(self.callable_factory, times=6).__call__(anyx())

    def test_get_passing_index_should_return_item_result_from_callable(self):
        self.tagSelection._initial_selection = set('abcdefghij')
        self.tag_mappings.update({'2': set('defg')})

        self.tagSelection.difference('2').get(2)
        verify(self.callable_factory, times=1).__call__(anyx())


class TestTagSelector(unittest.TestCase):

    def setUp(self):
        self.TagSelection = tagselection._TagSelection

    def tearDown(self):
        tagselection._TagSelection = self.TagSelection

    def test_get_should_return_tag_selection_instance(self):
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

    def test_register_should_add_reference_to_each_tag_set_in_tag_mappings(self):
        reference = 'REFERENCE'
        tags = ['TAG_A', 'TAG_B', 'TAG_C']

        class TagSelectionMock(object):

            def __init__(self, tag_mappings, *args, **kwargs):
                self._tag_mappings = tag_mappings

            def get_tag_mappings(self):
                return self._tag_mappings

            def union(self, *args, **kwargs):
                return self

        tagselection._TagSelection = TagSelectionMock

        selector = tagselection.TagSelector(None)
        selector.register(reference, tags)

        result = selector.get().get_tag_mappings()
        for tag in tags:
            assert reference in result[tag]

    def test_tags_should_return_reference_selection_instance(self):
        result = tagselection.TagSelector(None).tags()
        assert isinstance(result, tagselection._TagSelection)


def _process_dependencies(self, references):
    for key in references:
        if not self.registrations.get(key):
            self.registrations[key] = {}

        if not self.registrations[key].get('tags'):
            self.registrations[key]['tags'] = set()

        self.registrations[key]['tags'] |= self.manager.infere_tags(key)

# -*- coding: utf-8 -*-


import json
import functools
import itertools
import collections


class TagManager(object):

    def __init__(self, registrations):
        self._registrations = registrations
        self._mappings = []

    def infere_tags(self, reference):
        result = set()
        result.add(reference)

        if not self._registrations.get(reference) or not self._registrations[reference].get('dependencies'):
            return result

        for dependency_reference in self._registrations[reference]['dependencies']:

            dependency = self._registrations.get(dependency_reference)
            if not dependency:
                continue

            dependency_tags = dependency.get('tags')
            if not dependency_tags:
                continue

            for tag in dependency_tags:
                inherited_tag = ('{%s}' % tag) if tag[0] != '{' or tag[-1] != '}' else tag
                result.add(inherited_tag)

        return result

    def register(self, fn, *selections):
        if len(selections) is 0:
            return

        self._mappings.append((fn, selections))
        self._evaluate_current_selections(fn, selections)

    def register_synched(self, fn, selections, references=[]):
        if len(selections) is 0:
            self._execute_fn(fn, *references)
            return

        selection = selections[0]
        for reference in references:
            selection = selection.intersection('{%s}' % reference)

        def _wrapper(reference):
            self.register_synched(fn, selections[1:], references + [reference])

        self.register(_wrapper, selection)

    def evaluate_new_candidate(self, new_reference):
        for fn, selections in self._mappings:
            self._evaluate_existing_selections(fn, selections, new_reference)

    def _evaluate_existing_selections(self, fn, selections, new_reference):
        partial_elegible_references_list = []
        current_partial_references_list = []

        for selection in selections:
            partial_references_list_copy = None

            if selection.is_elegible(new_reference):
                partial_references_list_copy = current_partial_references_list[:]
                partial_references_list_copy.append([new_reference])

            references = [reference for reference in selection]
            current_partial_references_list.append(references)
            for partial_elegible_references in partial_elegible_references_list:
                partial_elegible_references.append(references)

            if partial_references_list_copy:
                partial_elegible_references_list.append(partial_references_list_copy)

        for elegible_references_list in partial_elegible_references_list:
            combinations = itertools.product(*elegible_references_list)
            for combination in combinations:
                self._execute_fn(fn, *combination)

    def _evaluate_current_selections(self, fn, selections):
        references = [[reference for reference in selection] for selection in selections]
        if len(references) is 0:
            return

        combinations = itertools.product(*references)
        for combination in combinations:
            self._execute_fn(fn, *combination)

    def _execute_fn(self, fn, *references):
        fn(*references)


class TagSelector(object):

    def __init__(self, callable_factory):
        self._callable_factory = callable_factory
        self._tag_mappings = collections.defaultdict(set)
        self._reference_mappings = collections.defaultdict(set)

    def register(self, reference, tags):
        self._reference_mappings[reference] = tags
        for tag in tags:
            self._tag_mappings[tag].add(reference)

    def get(self, *selectors):
        selection = _TagSelection(self._tag_mappings, self._callable_factory)
        return selection if len(selectors) is 0 else selection.union(*selectors)

    def tags(self, *references):
        selection = _TagSelection(self._reference_mappings, self.get)
        return selection if len(references) is 0 else selection.union(*references)


class _TagSelection(object):

    def __init__(self, tag_mappings, callable_factory, operations=[], initial=[]):
        self._tag_mappings = tag_mappings
        self._callable_factory = callable_factory
        self._operations = operations
        self._initial_selection = initial

    def __iter__(self):
        return iter(self._selection)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def __len__(self):
        return len(self._selection)

    def is_elegible(self, reference):
        return reference in self._selection

    def get(self, index=None):
        if index is not None:
            return self._callable_factory(sorted(self._selection)[index])

        result = {}
        for selected in sorted(self._selection):
            result[selected] = self._callable_factory(selected)
        return result

    def all(self):
        return _TagSelection(self._tag_mappings,
                             self._callable_factory,
                             [self._evaluate_all],
                             self._initial_selection)

    def union(self, *selectors):
        operation = functools.partial(self._evaluate_union, selectors)
        return _TagSelection(self._tag_mappings,
                             self._callable_factory,
                             self._operations + [operation],
                             self._initial_selection)

    def intersection(self, *selectors):
        operation = functools.partial(self._evaluate_intersection, selectors)
        return _TagSelection(self._tag_mappings,
                             self._callable_factory,
                             self._operations + [operation],
                             self._initial_selection)

    def difference(self, *selectors):
        operation = functools.partial(self._evaluate_difference, selectors)
        return _TagSelection(self._tag_mappings,
                             self._callable_factory,
                             self._operations + [operation],
                             self._initial_selection)

    def symmetric_difference(self, *selectors):
        operation = functools.partial(self._evaluate_symmetric_difference, selectors)
        return _TagSelection(self._tag_mappings,
                             self._callable_factory,
                             self._operations + [operation],
                             self._initial_selection)

    @property
    def _selection(self):
        selection = set(self._initial_selection)
        for operation in self._operations:
            selection = operation(selection)
        return selection

    def _evaluate_all(self, selection):
        group = set()
        for values in self._tag_mappings.itervalues():
            group |= values
        return group

    def _evaluate_union(self, selectors, selection):
        selection |= self._evaluate_selectors(*selectors)
        return selection

    def _evaluate_intersection(self, selectors, selection):
        selection &= self._evaluate_selectors(*selectors)
        return selection

    def _evaluate_difference(self, selectors, selection):
        selection -= self._evaluate_selectors(*selectors)
        return selection

    def _evaluate_symmetric_difference(self, selectors, selection):
        selection ^= self._evaluate_selectors(*selectors)
        return selection

    def _evaluate_selectors(self, *selectors):
        if len(selectors) is 0:
            return set()

        group = self._tag_mappings[selectors[0]].copy()
        for selector in selectors[1:]:
            group &= self._tag_mappings[selector]
        return group

    def _to_string(self):
        return '<selection %s currently-with="%s">' % (id(self), json.dumps(list(self._selection), indent=4))

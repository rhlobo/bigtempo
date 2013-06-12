import json
import functools
import collections


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
        return _TagSelection(self._tag_mappings, self._callable_factory).union(*selectors)

    def tags(self, *references):
        return _TagSelection(self._reference_mappings, self.get).union(*references)


class _TagSelection(object):

    def __init__(self, tag_mappings, callable_factory):
        self._tag_mappings = tag_mappings
        self._callable_factory = callable_factory
        self._operations = []
        self._initial_selection = []

    def __iter__(self):
        return iter(self._selection)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def is_elegible(self, reference):
        return reference in self._selection

    def get(self):
        result = {}
        for selected in self._selection:
            result[selected] = self._callable_factory(selected)
        return result

    def all(self):
        self._operations[:] = []
        self._operations.append(self._evaluate_all)
        return self

    def union(self, *selectors):
        operation = functools.partial(self._evaluate_union, selectors)
        self._operations.append(operation)
        return self

    def intersection(self, *selectors):
        operation = functools.partial(self._evaluate_intersection, selectors)
        self._operations.append(operation)
        return self

    def difference(self, *selectors):
        operation = functools.partial(self._evaluate_difference, selectors)
        self._operations.append(operation)
        return self

    def symmetric_difference(self, *selectors):
        operation = functools.partial(self._evaluate_symmetric_difference, selectors)
        self._operations.append(operation)
        return self

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
        group = self._tag_mappings[selectors[0]] if len(selectors) > 0 else set()
        for selector in selectors[1:]:
            group &= self._tag_mappings[selector]
        return group

    def _to_string(self):
        return json.dumps(list(self._selection), indent=4)

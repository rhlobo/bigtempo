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
        return '<selection %s currently-with="%s">' % (self.__repr__(), json.dumps(list(self._selection), indent=4))

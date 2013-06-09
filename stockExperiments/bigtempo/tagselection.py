import json
import collections


class TagSelector(object):

    def __init__(self, callable_factory):
        self._callable_factory = callable_factory
        self._tag_mappings = collections.defaultdict(set)

    def register(self, reference, tags):
        for tag in tags:
            self._tag_mappings[tag].add(reference)

    def get(self, *selectors):
        return _TagSelection(self._tag_mappings, self._callable_factory).union(*selectors)


class _TagSelection(object):

    def __init__(self, tag_mappings, callable_factory):
        self._tag_mappings = tag_mappings
        self._callable_factory = callable_factory
        self._selection = set()

    def __iter__(self):
        return iter(self._selection)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def _to_string(self):
        return json.dumps(list(self._selection), indent=4)

    def get(self):
        result = {}
        for selected in self._selection:
            result[selected] = self._callable_factory(selected)
        return result

    def all(self):
        group = set()
        for values in self._tag_mappings.itervalues():
            group |= values
        self._selection = group
        return self

    def union(self, *selectors):
        self._selection |= self._evaluate_selectors(*selectors)
        return self

    def intersection(self, *selectors):
        self._selection &= self._evaluate_selectors(*selectors)
        return self

    def difference(self, *selectors):
        self._selection -= self._evaluate_selectors(*selectors)
        return self

    def symmetric_difference(self, *selectors):
        self._selection ^= self._evaluate_selectors(*selectors)
        return self

    def _evaluate_selectors(self, *selectors):
        group = self._tag_mappings[selectors[0]] if len(selectors) > 0 else set()
        for selector in selectors[1:]:
            group &= self._tag_mappings[selector]
        return group

    def is_elegible(self, reference):
        raise NotImplementedError()

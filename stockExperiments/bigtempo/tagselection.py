import collections


class TagSelector(object):

    def __init__(self, callable_factory):
        self.callable_factory = callable_factory
        self.tag_mappings = collections.defaultdict(set)

    def register(self, reference, tags):
        for tag in tags:
            self.tag_mappings[tag].add(reference)

    def get(self, *selectors):
        return _TagSelection(self.tag_mappings, self.callable_factory).union(*selectors)


class _TagSelection(object):

    def __init__(self, tag_mappings, callable_factory):
        self.tag_mappings = tag_mappings
        self.callable_factory = callable_factory
        self.selection = set()

    def get(self):
        result = {}
        for selected in self.selection:
            result[selected] = self.callable_factory(selected)
        return result

    def all(self):
        group = set()
        for values in self.tag_mappings.itervalues():
            group |= values
        self.selection = group
        return self

    def union(self, *selectors):
        self.selection |= self._evaluate_selectors(*selectors)
        return self

    def intersection(self, *selectors):
        self.selection &= self._evaluate_selectors(*selectors)
        return self

    def difference(self, *selectors):
        self.selection -= self._evaluate_selectors(*selectors)
        return self

    def symmetric_difference(self, *selectors):
        self.selection ^= self._evaluate_selectors(*selectors)
        return self

    def _evaluate_selectors(self, *selectors):
        group = self.tag_mappings[selectors[0]] if len(selectors) > 0 else set()
        for selector in selectors[1:]:
            group &= self.tag_mappings[selector]
        return group

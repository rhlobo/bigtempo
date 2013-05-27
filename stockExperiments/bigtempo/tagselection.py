import colleactions.defaultdict as defaultdict


class TagSelector(object):

    def __init__(self, callable_factory):
        self.callable_factory = callable_factory
        self.tag_mappings = defaultdict(set)

    def register(self, reference, tags):
        for tag in tags:
            self.tag_mappings[tag].add(reference)

    def get(self, *selectors):
        return _TagSelection(self.tag_mappings, self.callable_factory).add(*selectors)


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

    def add(self, *selectors):
        self.selection |= self._evaluate_selectors(*selectors)
        return self

    def select(self, *selectors):
        self.selection &= self._evaluate_selectors(*selectors)
        return self

    def filter(self, *selectors):
        self.selection -= self._evaluate_selectors(*selectors)
        return self

    def _evaluate_selectors(self, *selectors):
        group = set()
        for selector in selectors:
            group &= self.tag_mappings.get(selector)
        return group

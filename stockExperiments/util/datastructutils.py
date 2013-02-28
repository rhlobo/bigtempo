

class LazyDict(object):

    def __init__(self, factory):
        self.c_dataMap = {}
        self.c_factory = factory

    def get(self, s_symbol):
        if self.c_dataMap.get(s_symbol) is None:
            self.c_dataMap[s_symbol] = self.c_factory.get()
        return self.c_dataMap[s_symbol]

    def keys(self):
        return self.c_dataMap.keys()


class ListFactory(object):

    def get(self):
        return []


class DictFactory(object):

    def get(self):
        return {}

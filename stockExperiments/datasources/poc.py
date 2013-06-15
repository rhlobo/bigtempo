from instances import data_engine


def for_synched(*selection):
    def wrapper(fn):
        reg(fn, selection)
        return fn
    return wrapper


def reg(fn, selections, references=[]):
    n = len(selections)
    if n is 0:
        fn(*references)
        return

    selection = selections[0]
    for reference in references:
        selection = selection.intersection('{%s}' % reference)

    @data_engine.for_each(selection)
    def wrapper(reference):
        reg(fn, selections[1:], references + [reference])


@for_synched(data_engine.select('RAW'),
             data_engine.select('RAW_PCT_CHANGE'),
             data_engine.select('RAW_NORMALIZATION_FACTOR'))
def bli(*refs):
    print '>> ',
    print refs



def slice(slicable, start=None, end=None):
    if start and end:
        return slicable[start:end]
    if start:
        return slicable[start:]
    if end:
        return slicable[:end]
    return slicable

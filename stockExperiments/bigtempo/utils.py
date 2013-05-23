

def slice_dataframe(dataframe, start, end):
    if start and end:
        return dataframe[start:end]
    if start:
        return dataframe[start:]
    if end:
        return dataframe[:end]
    return dataframe
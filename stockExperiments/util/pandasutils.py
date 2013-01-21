

def dataframe_to_list_of_lists(dataframe):
    result = []
    for i in range(len(dataframe)):
        row = []
        row.append(dataframe.ix[i].name)
        for j in dataframe.ix[i]:
            row.append(j)
        result.append(row)
    return result

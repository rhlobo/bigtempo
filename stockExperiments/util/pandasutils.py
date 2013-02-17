

def dataframe_to_list_of_lists(dataframe):
    result = []
    for index, c_row in dataframe.iterrows():
        row = [index]
        row.extend(list(c_row))
        result.append(row)
    return result

def data_converter(schema, data):
    """
    Applies schema to raw data to convert data to certain format
    If for some keys in schema can't find mapping in keys thats considered the key is None
    """
    obj = {}
    for key, value in schema.items():
        count = 0
        key_data = data
        try:
            while count < len(value):
                key_data = key_data.get("{}".format(value[count]))
                count += 1
            obj[key] = key_data
        except Exception:
            obj[key] = None
    return obj

def get_data(data, schema, field):
    data = data[field]
    parsed_data = data_converter(schema, data)
    return parsed_data

def get_data_list(data, schema, field):
    try:
        data = data[field]
        parsed_data = []
        for d in data:
            parsed = data_converter(schema, d)
            parsed_data.append(parsed)
        return list(parsed_data)
    except Exception as e:
        return []

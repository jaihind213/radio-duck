import datetime
from typing import List, Tuple


def deserialize_date_time(date_time: datetime.datetime) -> str:
    return date_time.isoformat()


def deserialize_date(dt: datetime.date) -> str:
    return dt.isoformat()


def mirror(x):
    return x


_deserialize_funcs = {
    "DATETIME": deserialize_date_time,
    "TIMESTAMP": deserialize_date_time,
    "TIMESTAMPTZ": deserialize_date_time,
    "TIMESTAMP WITH TIME ZONE": deserialize_date_time,
    "DATE": deserialize_date,
}

_non_serializable_datatypes = _deserialize_funcs.keys()


def jsonify_rows(schema: Tuple, rows) -> List:
    """
    datetime.datetime/date object cant be deserialized to json
    hence custom deserialization as string
    :param schema: tuple of string
    :param rows: list of tuples
    :return: rows with datatypes deserialized for json consumption
    """
    indexes = []
    for i, data_type in enumerate(schema):
        if data_type.upper() in _non_serializable_datatypes:
            indexes.append(i)

    if len(indexes) == 0:
        return rows

    modified_rows = rows
    for index in indexes:

        def format_data_type_in_tuple(input_tuple, index=index, schema=schema):
            data_type = schema[index]
            deser_func = _deserialize_funcs.get(data_type.upper(), mirror)
            modified_tuple = list(input_tuple)
            modified_tuple[index] = deser_func(modified_tuple[index])
            return tuple(modified_tuple)

        modified_rows = list(map(format_data_type_in_tuple, modified_rows))

    return modified_rows

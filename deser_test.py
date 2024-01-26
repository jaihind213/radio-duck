from collections import Counter
from datetime import date, datetime

import pytz

import deser


def test_deserialize_date_time():
    assert "2023-01-01T15:14:13", deser.deserialize_date_time(
        datetime(2023, 1, 1, 15, 14, 13)
    )


def test_deserialize_date():
    assert "2023-01-01", deser.deserialize_date(date(2023, 1, 1))


def test_jsonify_rows_regular_types():
    input_rows = ["vishnu"]

    modified_rows = deser.jsonify_rows(("string",), input_rows)

    assert Counter(input_rows) == Counter(modified_rows)


def test_jsonify_rows():
    dtime = datetime(2023, 1, 1, 15, 14, 13)
    dt = date(2023, 1, 1)
    input_rows = [("vishnu", dtime, dt, dtime), ("roque", dtime, dt, dtime)]
    schema = ("string", "datetime", "date", "timestamp")

    print(dtime.isoformat())

    modified_rows = deser.jsonify_rows(schema, input_rows)
    xpected = [
        ("vishnu", dtime.isoformat(), dt.isoformat(), dtime.isoformat()),
        ("roque", dtime.isoformat(), dt.isoformat(), dtime.isoformat()),
    ]
    assert Counter(xpected) == Counter(modified_rows)


def test_deserialize_date_time_with_zone():
    d = datetime(
        2023, month=1, day=1, hour=1, minute=1, second=1, tzinfo=pytz.utc
    )
    input_rows = [(d, d)]
    schema = ("TIMESTAMP WITH TIME ZONE", "TIMESTAMPTZ")

    modified_rows = deser.jsonify_rows(schema, input_rows)

    assert Counter([(d.isoformat(), d.isoformat())]) == Counter(modified_rows)

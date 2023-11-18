from __future__ import annotations

from sqlalchemy.dialects import registry

from superset.db_engine_specs.duckdb import DuckDBEngineSpec


class RadioDuckEngineSpec(DuckDBEngineSpec):
    engine = "district5"
    engine_name = "Radio-Duck"

    sqlalchemy_uri_placeholder = "radio_duck+district5://user:pass@localhost:8000/?api=/v1/sql/&scheme=http"  # noqa: E501,B950
    registry.register(
        "radio_duck.district5", "radio_duck.sqlalchemy", "RadioDuckDialect"
    )

"""Utility classes and functions."""

from typing import Any


class SingletonMeta(type):
    """Metaclass for implementing singleton pattern."""

    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def build_update_query(table_name: str, columns: str, id_value: Any, **kwargs) -> tuple[str, list]:
    """Build a dynamic UPDATE query with RETURNING clause.

    Args:
        table_name: Name of the table to update
        columns: Comma-separated list of columns to return
        id_value: The ID value for the WHERE clause
        **kwargs: Column-value pairs to update

    Returns:
        Tuple of (query_string, values_list)
    """
    set_clauses = []
    values = []
    param_num = 1

    for key, value in kwargs.items():
        set_clauses.append(f"{key} = ${param_num}")
        values.append(value)
        param_num += 1

    values.append(id_value)
    query = f"""
        UPDATE {table_name}
        SET {", ".join(set_clauses)}
        WHERE id = ${param_num}
        RETURNING {columns}
    """

    return query, values

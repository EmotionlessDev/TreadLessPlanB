import sqlite3
from typing import Any, List, Tuple


class Database:
    """A simple SQLite database handler."""

    def __init__(self) -> None:
        """Initialize the database connection."""

    def create_table(self, table_name: str, columns: str) -> None:
        """Create a table with the given name and columns."""
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.conn.commit()

    def insert_data(self, table_name: str, data: Tuple[Any, ...]) -> None:
        """Insert a row of data into the specified table."""
        placeholders = ", ".join(["?"] * len(data))
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        self.conn.commit()

    def fetch_data(
        self, query: str, params: Tuple[Any, ...] = ()
    ) -> List[Tuple[Any, ...]]:
        """Fetch data based on a given query and parameters."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self) -> None:
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()

    def connect(self, db_name: str) -> None:
        """Open the database connection."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

"""
Database connection utilities for Cricbuzz LiveStats.
Supports SQLite (default) with easy extension to PostgreSQL/MySQL.
"""

import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path

# Default DB path (relative to project root)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "cricbuzz.db"


def get_connection(db_path: str = None):
    """
    Create and return a SQLite connection with row factory enabled.
    """
    path = db_path or str(DB_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_db_cursor(db_path: str = None):
    """Context manager yielding a cursor; commits on success, rolls back on error."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query: str, params: tuple = None, fetch: str = "all"):
    """
    Execute a SQL query and return results.
    fetch: 'all' | 'one' | 'none'
    """
    with get_db_cursor() as cur:
        cur.execute(query, params or ())
        if fetch == "all":
            return [dict(row) for row in cur.fetchall()]
        elif fetch == "one":
            row = cur.fetchone()
            return dict(row) if row else None
        return None


def execute_write(query: str, params: tuple = None):
    """Execute INSERT / UPDATE / DELETE and return lastrowid / rowcount."""
    with get_db_cursor() as cur:
        cur.execute(query, params or ())
        return {"lastrowid": cur.lastrowid, "rowcount": cur.rowcount}


def init_db(force: bool = False):
    """Create all tables if they do not exist (or drop & recreate if force=True)."""
    schema_path = BASE_DIR / "sql" / "schema.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    try:
        if force:
            # Drop existing tables carefully (reverse dependency order)
            conn.executescript("""
                DROP TABLE IF EXISTS partnerships;
                DROP TABLE IF EXISTS fielding_stats;
                DROP TABLE IF EXISTS bowling_stats;
                DROP TABLE IF EXISTS batting_stats;
                DROP TABLE IF EXISTS match_players;
                DROP TABLE IF EXISTS matches;
                DROP TABLE IF EXISTS series;
                DROP TABLE IF EXISTS venues;
                DROP TABLE IF EXISTS players;
                DROP TABLE IF EXISTS teams;
            """)
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db(force=True)
    print(f"Database initialized at {DB_PATH}")

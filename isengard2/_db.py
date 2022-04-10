from typing import Iterator
from contextlib import contextmanager
from sqlite3 import connect as sqlite3_connect, Connection, OperationalError
from pathlib import Path

from ._exceptions import IsengardDBError


DB_VERSION = 1
# This magic number has two roles:
# - it makes unlikely we mistakenly consider an unrelated database as a legit
#   Isengard database
# - it acts as a constant ID to easily retrieve the single row in the `version` table
VERSION_MAGIC_NUMBER = 76388


SQL_CREATE_VERSION_TABLE = f"""
CREATE TABLE IF NOT EXISTS version(
    magic INT NOT NULL UNIQUE DEFAULT {VERSION_MAGIC_NUMBER},
    value INT NOT NULL
)"""


SQL_CREATE_OBJS_TABLE = """
CREATE TABLE IF NOT EXISTS objs(
    _id SERIAL PRIMARY KEY,
    value INT NOT NULL
)"""


SQL_INIT_VERSION_ROW = "INSERT INTO version(value) VALUES(?)"
SQL_FETCH_VERSION_ROW = f"SELECT value FROM version WHERE magic = {VERSION_MAGIC_NUMBER}"


def init_or_reset_db(path: Path):
    try:
        con = sqlite3_connect(path)
    except OperationalError as exc:
        raise IsengardDBError(f"Cannot open/create database at {path}: {exc}") from exc

    # Optimistic check: the database is already initialized in the correct version
    try:
        cur = con.execute(SQL_FETCH_VERSION_ROW)
        current_db_version,  = cur.fetchone()
    except OperationalError as exc:
        # Just consider the database is invalid
        current_db_version = -1

    if current_db_version != DB_VERSION:
        # DB is not compatible with us, destroy it an restart anew
        con.close()

        try:
            path.unlink()
        except FileNotFoundError:
            pass
        except Exception as exc:
            raise IsengardDBError(f"Cannot delete incompatible database at {path}: {exc}") from exc

        try:
            con = sqlite3_connect(path)
            with con:
                cur = con.cursor()
                cur.execute(SQL_CREATE_VERSION_TABLE)
                cur.execute(SQL_CREATE_OBJS_TABLE)
                cur.execute(SQL_INIT_VERSION_ROW, (DB_VERSION, ))
        except OperationalError as exc:
            raise IsengardDBError(f"Cannot recreate database at {path}: {exc}") from exc

    return con


class DB:
    def __init__(self, path: Path, con: Connection):
        self.path = path
        self.con = sqlite3_connect(path)

    @classmethod
    @contextmanager
    def connect(cls, path: Path) -> Iterator["DB"]:
        con = init_or_reset_db(path)
        try:
            yield cls(path, con)
        finally:
            con.close()

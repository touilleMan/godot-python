import pytest
import sqlite3
from contextlib import contextmanager

from .._exceptions import IsengardDBError
from .._db import DB, DB_VERSION


@contextmanager
def db_cursor(db_path):
    con = sqlite3.connect(db_path)
    with con:
        yield con.cursor()
    con.close()


def assert_db_version(db_path):
    with db_cursor(db_path) as cur:
        row = cur.execute("SELECT value FROM version WHERE magic = 76388").fetchone()
    assert row[0] == DB_VERSION


def create_canary(db_path):
    with db_cursor(db_path) as cur:
        cur.execute("CREATE TABLE canary (_id SERIAL)")
    assert_canary(db_path)  # Sanity check


def assert_canary(db_path, expected="present"):
    with db_cursor(db_path) as cur:
        try:
            cur.execute("SELECT * FROM canary")
            outcome = "present"
        except sqlite3.OperationalError:
            # Should raise OperationalError if table doesn't exists anymore
            outcome = "missing"
    assert outcome == expected


def test_base(tmp_path):
    db_path = tmp_path / "db.sqlite"
    with DB.connect(path=db_path):
        pass
    assert_db_version(db_path)


def test_reset_db(tmp_path):
    db_path = tmp_path / "db.sqlite"
    # Create DB
    with DB.connect(path=db_path):
        pass
    assert_db_version(db_path)

    # Add custom data to the database to be able to tell if it has been overwritten
    create_canary(db_path)

    # DB is valid, should not be re-created or modified
    with DB.connect(path=db_path):
        pass
    assert_db_version(db_path)

    # Ensure canary is still there
    assert_canary(db_path)


def test_incompatible_db_version(tmp_path):
    db_path = tmp_path / "db.sqlite"
    # Create DB
    with DB.connect(path=db_path):
        pass

    with db_cursor(db_path) as cur:
        cur.execute(f"UPDATE version SET value = {DB_VERSION + 1} WHERE magic = 76388")
    create_canary(db_path)

    # Re-create DB given version doesn't match
    with DB.connect(path=db_path):
        pass
    assert_db_version(db_path)
    assert_canary(db_path, expected="missing")


@pytest.mark.parametrize("with_version_table", (False, True))
def test_unrelated_db(tmp_path, with_version_table):
    db_path = tmp_path / "db.sqlite"
    # Create a dummy database
    with db_cursor(db_path) as cur:
        cur.execute("CREATE TABLE user (email TEXT)")
        if with_version_table:
            cur.execute("CREATE TABLE version (value INT)")
    create_canary(db_path)

    # Create DB, should overwrite the dummy one
    with DB.connect(path=db_path):
        pass
    assert_db_version(db_path)
    assert_canary(db_path, expected="missing")


def test_invalid_db_path(tmp_path):
    # Path is a directory
    with pytest.raises(IsengardDBError):
        with DB.connect(path=tmp_path):
            pass

    # Path contains not existing parent directory
    with pytest.raises(IsengardDBError):
        with DB.connect(path=tmp_path / "foo/bar.sqlite"):
            pass

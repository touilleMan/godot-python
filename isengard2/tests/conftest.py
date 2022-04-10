import pytest
import sqlite3
from pathlib import Path


@pytest.fixture
def memory_sqlite3(monkeypatch):
    def patched_sqlite3_connect(path: Path) -> sqlite3.Connection:
        uri = f"{path.as_uri()}?mode=memory&cache=shared"
        return sqlite3.connect(uri, uri=True)

    monkeypatch.setattr(".._db.sqlite3_connect", patched_sqlite3_connect)

import pytest
from typing import Optional, Callable, List, Dict
import inspect
import sqlite3
from pathlib import Path

from .. import _db
from .._api import Isengard
from .._const import ConstTypes
from .._runner import Runner
from .._target import TargetHandlersBundle, FileTargetHandler, ConfiguredTargetID
from .._rule import ConfiguredRule


@pytest.fixture
def memory_sqlite3(monkeypatch):
    def patched_sqlite3_connect(path: Path) -> sqlite3.Connection:
        uri = f"{path.absolute().as_uri()}?mode=memory&cache=shared"
        return sqlite3.connect(uri, uri=True)

    monkeypatch.setattr(_db, "sqlite3_connect", patched_sqlite3_connect)


@pytest.fixture
def target_handlers_bundle():
    return TargetHandlersBundle(
        target_handlers=Isengard.DEFAULT_TARGET_HANDLERS,
    )


@pytest.fixture
def rule_factory(tmp_path: Path):
    def _rule_factory(
        configured_outputs: List[ConfiguredTargetID],
        id: Optional[str] = None,
        fn: Optional[Callable] = None,
        configured_inputs: Optional[List[ConfiguredTargetID]] = None,
        workdir: Optional[Path] = None,
    ):
        if not fn:

            def fn(outputs):
                for output in outputs:
                    output.touch()

        if fn:
            signature = inspect.signature(fn)
            params = {s.name for s in signature.parameters.values()}

        assert configured_outputs
        configured_inputs = configured_inputs or []
        return ConfiguredRule(
            workdir=workdir or tmp_path,
            id=id or f"rule-{configured_outputs[0].rsplit('/', 1)[1]}",
            fn=fn,
            params=params,
            outputs=configured_outputs,
            inputs=configured_inputs,
            configured_outputs=configured_outputs,
            configured_inputs=configured_inputs,
        )

    return _rule_factory


@pytest.fixture
def runner_factory(tmp_path: Path):
    def _runner_factory(
        rules: List[ConfiguredRule],
        config: Optional[Dict[str, ConstTypes]] = None,
        target_handlers: Optional[TargetHandlersBundle] = None,
        db_path: Optional[Path] = None,
    ):
        target_handlers = TargetHandlersBundle([FileTargetHandler()])
        return Runner(
            rules={r.id: r for r in rules},
            config=config or {},
            target_handlers=target_handlers,
            db_path=db_path or tmp_path / "db.sqlite",
        )

    return _runner_factory


def configurify(path: Path, discriminant: str = "#") -> ConfiguredTargetID:
    return ConfiguredTargetID(path.resolve().as_posix() + discriminant)

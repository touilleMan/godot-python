import pytest
import time
from typing import Dict
from pathlib import Path

from .._target import (
    ConstTypes,
    UnresolvedTargetID,
    ResolvedTargetID,
    BaseTargetHandler,
    FileTargetHandler,
    FolderTargetHandler,
    VirtualTargetHandler,
    DeferredTargetHandler,
)


@pytest.fixture(
    params=[FileTargetHandler, FolderTargetHandler],
    ids=["file", "folder"],
)
def fs_based_target_handler(request):
    return request.param()


@pytest.fixture(
    params=[
        VirtualTargetHandler,
        DeferredTargetHandler,
    ],
    ids=[
        "virtual",
        "deferred",
    ],
)
def non_fs_based_target_handler(request):
    return request.param()


@pytest.mark.parametrize("kind", ["absolute", "relative"])
def test_fs_based_target_handlers_resolve(fs_based_target_handler: BaseTargetHandler, kind):
    handler = fs_based_target_handler
    assert handler.DISCRIMINANT_SUFFIX

    id = "{a}/{b}/spam" + handler.DISCRIMINANT_SUFFIX
    config: Dict[str, ConstTypes] = {"a": 1, "b": "bay"}
    expected_resolved_path = "/foo/bar/1/bay/spam"
    if kind == "absolute":
        id = "/foo/bar/" + id
        workdir = Path("/whatever/")
    else:
        assert kind == "relative"
        workdir = Path("/foo/bar/")

    resolved = handler.resolve(id=UnresolvedTargetID(id), config=config, workdir=workdir)
    assert resolved == str(expected_resolved_path) + handler.DISCRIMINANT_SUFFIX


def test_non_fs_based_target_handlers_resolve(non_fs_based_target_handler: BaseTargetHandler):
    handler = non_fs_based_target_handler
    assert handler.DISCRIMINANT_SUFFIX

    workdir = Path("/foo/bar")
    config: Dict[str, ConstTypes] = {"a": 1, "b": "bay"}
    id = "{a}/{b}/spam" + handler.DISCRIMINANT_SUFFIX

    resolved = handler.resolve(id=UnresolvedTargetID(id), config=config, workdir=workdir)
    assert resolved == "1/bay/spam" + handler.DISCRIMINANT_SUFFIX


def test_virtual_target_handler_cook_and_co():
    handler = VirtualTargetHandler()
    resolved = ResolvedTargetID("foo@")

    # 1) Cook
    cooked = handler.cook(id=resolved, previous_fingerprint=None)
    assert cooked == "foo@"

    # 2) Compute fingerprint
    assert handler.compute_fingerprint(cooked) is None
    assert handler.need_rebuild(cooked, previous_fingerprint=b"dummy") is True

    # 3) Clean
    handler.clean(cooked)


@pytest.mark.parametrize("kind", ["file", "folder"])
def test_deferred_target_handler_cook_fs_based(tmp_path, kind):
    # 1) Cook
    handler = DeferredTargetHandler()
    cooked = handler.cook(ResolvedTargetID("foo?"), previous_fingerprint=None)
    assert isinstance(cooked, handler.TARGET_TYPE)
    assert cooked.resolved is None

    # 2) Actual resolve
    resolved_cooked = tmp_path / "foo"
    if kind == "file":
        resolved_handler = FileTargetHandler()
        create_resolved_cooked = resolved_cooked.touch
    else:
        assert kind == "folder"
        resolved_handler = FolderTargetHandler()
        create_resolved_cooked = resolved_cooked.mkdir
    cooked.resolve(resolved_cooked, resolved_handler)

    # 3) Compute fingerprint
    nop_fingerprint = handler.compute_fingerprint(cooked)
    nop_refingerprint = handler.compute_fingerprint(cooked)
    assert nop_refingerprint == nop_fingerprint

    create_resolved_cooked()

    fingerprint = handler.compute_fingerprint(cooked)
    assert fingerprint != nop_fingerprint
    refingerprint = handler.compute_fingerprint(cooked)
    assert refingerprint == fingerprint

    assert handler.need_rebuild(cooked, previous_fingerprint=b"dummy") is True
    assert handler.need_rebuild(cooked, previous_fingerprint=refingerprint) is False

    # 4) Clean
    handler.clean(cooked)
    assert not resolved_cooked.exists()
    handler.clean(cooked)  # Idempotent

    # 5) Bonus: cook with fingerprint resolve automatically !
    cooked = handler.cook(ResolvedTargetID("foo?"), previous_fingerprint=fingerprint)
    assert cooked.resolved[0] == resolved_cooked
    assert isinstance(cooked.resolved[1], type(resolved_handler))
    # Broken fingerprint
    cooked = handler.cook(ResolvedTargetID("foo?"), previous_fingerprint=b"foo")
    assert cooked.resolved is None
    # Fingerprint on unresolved
    unresolved_cooked = handler.cook(ResolvedTargetID("foo?"), previous_fingerprint=None)
    unresolved_fingerprint = handler.compute_fingerprint(unresolved_cooked)
    cooked = handler.cook(ResolvedTargetID("foo?"), previous_fingerprint=unresolved_fingerprint)
    assert cooked.resolved is None


def test_deferred_target_handler_cook_unresolved():
    # 1) Cook
    handler = DeferredTargetHandler()
    cooked = handler.cook(ResolvedTargetID("foo?"), previous_fingerprint=None)
    assert isinstance(cooked, handler.TARGET_TYPE)

    # 2) Compute fingerprint
    assert handler.compute_fingerprint(cooked) is None
    assert handler.need_rebuild(cooked, previous_fingerprint=b"dummy") is True

    # 3) Clean
    handler.clean(cooked)
    handler.clean(cooked)  # Idempotent


def test_file_target_handler_compute_fingerprint(tmp_path):
    handler = FileTargetHandler()
    cooked = tmp_path / "foo.txt"
    # No file
    assert handler.compute_fingerprint(cooked) is None
    # Folder instead of expected file
    cooked.mkdir()
    assert handler.compute_fingerprint(cooked) is None
    cooked.rmdir()
    # File v1
    cooked.write_text("v1")
    fingerprint1 = handler.compute_fingerprint(cooked)
    assert fingerprint1 is not None
    # File v2
    cooked.write_text("v2")
    fingerprint2 = handler.compute_fingerprint(cooked)
    assert fingerprint2 is not None
    # Same data, different timestamp
    mtime1 = cooked.stat().st_mtime
    time.sleep(0.01)  # mtime may not get modified if 2nd touch is too soon
    cooked.touch()
    mtime2 = cooked.stat().st_mtime
    assert mtime1 != mtime2
    refingerprint2 = handler.compute_fingerprint(cooked)
    assert refingerprint2 is not None
    assert fingerprint2 != refingerprint2

    # Check need rebuild
    assert handler.need_rebuild(cooked, previous_fingerprint=fingerprint2) is True
    assert handler.need_rebuild(cooked, previous_fingerprint=refingerprint2) is False


def test_folder_target_handler_compute_fingerprint(tmp_path):
    handler = FolderTargetHandler()
    cooked = tmp_path / "foo"
    # No folder
    assert handler.compute_fingerprint(cooked) is None
    # File instead of expected folder
    cooked.touch()
    assert handler.compute_fingerprint(cooked) is None
    cooked.unlink()
    # Folder exists
    cooked.mkdir()
    fingerprint = handler.compute_fingerprint(cooked)
    assert fingerprint is not None
    # Folder exists, but different timestamp
    mtime1 = cooked.stat().st_mtime
    time.sleep(0.01)  # mtime may not get modified if 2nd touch is too soon
    cooked.touch()
    mtime2 = cooked.stat().st_mtime
    assert mtime1 != mtime2
    refingerprint = handler.compute_fingerprint(cooked)
    assert refingerprint is not None
    assert fingerprint != refingerprint

    # Check need rebuild
    assert handler.need_rebuild(cooked, previous_fingerprint=fingerprint) is True
    assert handler.need_rebuild(cooked, previous_fingerprint=refingerprint) is False


def test_fs_based_target_handlers_cook_and_co(tmp_path, fs_based_target_handler: BaseTargetHandler):
    handler = fs_based_target_handler
    id = UnresolvedTargetID(str(tmp_path / "foo") + handler.DISCRIMINANT_SUFFIX)
    resolved = handler.resolve(id=id, config={}, workdir=Path("/"))

    # 1) Cook
    cooked = handler.cook(id=resolved, previous_fingerprint=None)
    assert cooked == Path(id[:-1])
    recooked = handler.cook(id=resolved, previous_fingerprint=b"dummy")
    assert recooked == cooked

    # 2) Compute fingerprint
    assert not cooked.exists()
    assert handler.compute_fingerprint(cooked) is None
    if isinstance(handler, FileTargetHandler):
        cooked.write_text("v1")
        assert cooked.exists()
    else:
        assert isinstance(handler, FolderTargetHandler)
        cooked.mkdir()
    fingerprint = handler.compute_fingerprint(cooked)
    assert fingerprint is not None
    refingerprint = handler.compute_fingerprint(cooked)
    assert refingerprint == fingerprint

    # 3) Clean
    handler.clean(cooked)
    assert not cooked.exists()
    handler.clean(cooked)  # Clean is idempotent

import pytest
import time
from typing import Dict
from pathlib import Path

from .._target import (
    ConstTypes,
    RawTargetID,
    ConfiguredTargetID,
    BaseTargetHandler,
    FileTargetHandler,
    FolderTargetHandler,
    VirtualTargetHandler,
    DeferredTargetHandler,
    TargetHandlersBundle,
)
from .._exceptions import IsengardRunError, IsengardConsistencyError


@pytest.fixture(
    params=[FileTargetHandler, FolderTargetHandler],
    ids=["file", "folder"],
)
def fs_based_target_handler(request):
    return request.param()


@pytest.mark.parametrize("kind", ["absolute", "relative"])
def test_fs_based_target_handlers_configure(fs_based_target_handler: BaseTargetHandler, kind):
    handler = fs_based_target_handler
    assert handler.DISCRIMINANT

    id = "{a}/{b}/spam" + handler.DISCRIMINANT
    config: Dict[str, ConstTypes] = {"a": 1, "b": "bay"}
    expected_configured_path = "/foo/bar/1/bay/spam"
    if kind == "absolute":
        id = "/foo/bar/" + id
        workdir = Path("/whatever/")
    else:
        assert kind == "relative"
        workdir = Path("/foo/bar/")

    configured = handler.configure(id=RawTargetID(id), config=config, workdir=workdir)
    assert configured == str(expected_configured_path) + handler.DISCRIMINANT


@pytest.mark.parametrize("kind", ["virtual", "deferred"])
def test_non_fs_based_target_handlers_configure(target_handlers_bundle, kind):
    if kind == "virtual":
        handler = VirtualTargetHandler()
    else:
        assert kind == "deferred"
        handler = DeferredTargetHandler(target_handlers_bundle)
    assert handler.DISCRIMINANT

    workdir = Path("/foo/bar")
    config: Dict[str, ConstTypes] = {"a": 1, "b": "bay"}
    id = "{a}/{b}/spam" + handler.DISCRIMINANT

    configured = handler.configure(id=RawTargetID(id), config=config, workdir=workdir)
    assert configured == "1/bay/spam" + handler.DISCRIMINANT


def test_virtual_target_handler_cook_and_co():
    handler = VirtualTargetHandler()
    configured = ConfiguredTargetID("foo@")

    # 1) Cook
    cooked = handler.cook(id=configured, previous_fingerprint=None)
    assert cooked == "foo@"

    # 2) Compute fingerprint
    assert handler.compute_fingerprint(cooked) is None
    assert handler.need_rebuild(cooked, previous_fingerprint=b"dummy") is True

    # 3) Clean
    handler.clean(cooked)


@pytest.mark.parametrize("kind", ["file", "folder"])
def test_deferred_target_handler_cook_fs_based(tmp_path, target_handlers_bundle, kind):
    # 1) Cook
    handler = DeferredTargetHandler(target_handlers_bundle)
    cooked = handler.cook(ConfiguredTargetID("foo?"), previous_fingerprint=None)
    assert isinstance(cooked, handler.COOKED_TYPE)
    expected_err = r"Deferred target `foo\?` not resolved yet !"
    with pytest.raises(IsengardRunError, match=expected_err):
        cooked.resolved

    # 2) Actual resolve
    resolved_cooked = tmp_path / "foo"
    if kind == "file":
        resolved_discriminant = "#"
        create_resolved_cooked = resolved_cooked.touch
    else:
        assert kind == "folder"
        resolved_discriminant = "/"
        create_resolved_cooked = resolved_cooked.mkdir
    cooked.resolve(resolved_cooked, resolved_discriminant)

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
    cooked = handler.cook(ConfiguredTargetID("foo?"), previous_fingerprint=fingerprint)
    assert cooked.resolved == resolved_cooked
    # Resolve from fingerprint can be re-resolved...
    cooked.resolve(
        "<resolved_as_virtual>", "@"
    )  # Resolution doesn't even have to be of the same discriminant
    assert cooked.resolved == "<resolved_as_virtual>"
    # ...unlike regular resolve that can be only donc once
    expected_err = r"Deferred target `foo\?` already resolved !"
    with pytest.raises(IsengardRunError, match=expected_err):
        cooked.resolve("<resolved_as_virtual>", "@")
    # Broken fingerprint
    cooked = handler.cook(ConfiguredTargetID("foo?"), previous_fingerprint=b"foo")
    expected_err = r"Deferred target `foo\?` not resolved yet !"
    with pytest.raises(IsengardRunError, match=expected_err):
        cooked.resolved


def test_deferred_target_handler_cook_unresolved(target_handlers_bundle):
    # 1) Cook
    handler = DeferredTargetHandler(target_handlers_bundle)
    cooked = handler.cook(ConfiguredTargetID("foo?"), previous_fingerprint=None)
    assert isinstance(cooked, handler.COOKED_TYPE)

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
    id = RawTargetID(str(tmp_path / "foo") + handler.DISCRIMINANT)
    configured = handler.configure(id=id, config={}, workdir=Path("/"))

    # 1) Cook
    cooked = handler.cook(id=configured, previous_fingerprint=None)
    assert cooked == Path(id[:-1])
    recooked = handler.cook(id=configured, previous_fingerprint=b"dummy")
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


def test_bundle_configure_target_with_invalid_suffix(target_handlers_bundle: TargetHandlersBundle):
    excepted_err = r"Invalid/missing discriminant suffix for target `foo`, accepted discriminants: `\?`, `#`, `/`, `@`"
    with pytest.raises(IsengardConsistencyError, match=excepted_err):
        target_handlers_bundle.configure_target(
            target="foo",
            config={},
            workdir=Path("/foo/bar"),
        )

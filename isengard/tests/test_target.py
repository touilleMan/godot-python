import pytest
from pathlib import Path

from isengard import (
    FileTarget,
    FolderTarget,
    VirtualTarget,
    ConfiguredVirtualTarget,
    IsengardDefinitionError,
)


@pytest.mark.parametrize("target_cls", [FileTarget, FolderTarget])
@pytest.mark.parametrize(
    "label,expected_relative,config",
    [
        ("foo", "foo", {}),  # Empty config
        ("foo", "foo", {"foo": "bar"}),  # Unused config value
        ("{bar}/foo", "spam/foo", {"bar": "spam"}),  # Config resolution
        (
            "a/b/{bar}/c/d/../e",
            "a/c/e",
            {"bar": "../x/../"},
        ),  # Relative path resolution
        ("/foo", "/foo", {}),  # Absolute path
        ("{bar}/foo", "/bar/foo", {"bar": "/bar"}),  # Absolute path in config
    ],
)
def test_fs_target_configure(tmp_path, target_cls, label, expected_relative, config):
    if expected_relative.startswith("/"):
        expected = Path(expected_relative).resolve().absolute()
    else:
        expected = (tmp_path / expected_relative).resolve().absolute()
    target = target_cls(label=label, workdir=tmp_path)
    configured = target.configure(**config)
    assert isinstance(configured, Path)
    assert configured == expected


@pytest.mark.parametrize("target_cls", [FileTarget, FolderTarget])
def test_fs_target_configure_with_missing(tmp_path, target_cls):
    target = target_cls(label="foo/{bar}", workdir=tmp_path)
    with pytest.raises(IsengardDefinitionError):
        target.configure()


def test_virtual_target_configure(tmp_path):
    target = VirtualTarget(label="foo/{bar}", workdir=tmp_path)
    lazy = target.configure(bar="42")
    assert isinstance(lazy, ConfiguredVirtualTarget)
    assert lazy == "foo/42"


@pytest.mark.parametrize("target_cls", [VirtualTarget, FileTarget, FolderTarget])
def test_generate_fingerprint(tmp_path, target_cls):
    target = target_cls(label="foo", workdir=tmp_path)
    configured = target.configure()
    # Fingerprint is idempotent
    f1 = target.generate_fingerprint(configured)
    f2 = target.generate_fingerprint(configured)
    assert f1 == f2

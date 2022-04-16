import pytest
from pathlib import Path
import time
import sys

from .._runner import Runner

from .conftest import resolvify


def test_run_single_output(tmp_path: Path, runner_factory, rule_factory):
    target_path = tmp_path / "target.txt"
    resolved_target = resolvify(target_path)

    def fn(output, used):
        # Remove file before writting it to ensure ctime AND mtime are modified
        try:
            output.unlink()
        except FileNotFoundError:
            pass
        output.write_text(str(time.monotonic()))

    rules = [
        rule_factory(
            fn=fn,
            resolved_outputs=[resolved_target],
        ),
    ]
    config = {"used": 1, "unused": 1}
    runner: Runner = runner_factory(
        rules=rules,
        config=config,
    )

    last_mtime = None  # last modification of file content
    last_content = None

    def assert_has_changed():
        nonlocal last_mtime, last_content

        new_content = target_path.read_text()
        assert new_content != last_content

        new_stats = target_path.stat()
        assert new_stats.st_mtime != last_mtime

        last_mtime = new_stats.st_mtime
        last_content = new_content

    def assert_has_not_changed():
        assert target_path.read_text() == last_content
        stats = target_path.stat()
        assert stats.st_mtime == last_mtime

    def wait_beyond_mtime_resolution_atomicity():
        # Time resolution for mtime depend on OS/FS and can be suprisingly long
        # (e.g. Windows/FAT32 has a 2-second resolution for mtime !)
        # Create a brand new file, and wait until we can change it mtime/ctime.
        # This is to ensure any file created before will have it mtime/ctime updated
        # on file modification.
        file = tmp_path / f"stat-resolution-{time.monotonic()}"
        file.write_text("whatever")
        stats = file.stat()
        for i in range(30):
            time.sleep(0.01)
            file.unlink()
            file.write_text("whatever")  # recreate should update mtime and ctime
            stats2 = file.stat()
            if stats2.st_mtime != stats.st_mtime:
                break
        else:
            raise AssertionError(
                "Waited too long for mtime changes, you OS/FS might have a very long long time resolution"
            )

    # Run the rule
    runner.run(resolved_target)
    assert target_path.exists()
    stats = target_path.stat()
    last_ctime = stats.st_ctime
    last_mtime = stats.st_mtime
    last_content = target_path.read_text()

    # Re-running should be a noop
    runner.run(resolved_target)
    assert_has_not_changed()

    # If mtime has changed, rule should be rerun
    wait_beyond_mtime_resolution_atomicity()
    target_path.write_text(last_content)
    assert target_path.stat().st_mtime != last_mtime
    wait_beyond_mtime_resolution_atomicity()
    runner.run(resolved_target)
    assert_has_changed()

    # If content has changed, of course rule should be rerun !
    wait_beyond_mtime_resolution_atomicity()
    target_path.write_text("whatever")
    wait_beyond_mtime_resolution_atomicity()
    runner.run(resolved_target)
    assert_has_changed()

    # Using another runner should not change anything
    wait_beyond_mtime_resolution_atomicity()
    other_runner: Runner = runner_factory(rules=rules, config=config)
    other_runner.run(resolved_target)
    assert_has_not_changed()

    # If config has changed, rule should be rerun...
    wait_beyond_mtime_resolution_atomicity()
    config2 = config.copy()
    config2["used"] += 1
    runner_config_changed: Runner = runner_factory(rules=rules, config=config2)
    runner_config_changed.run(resolved_target)
    assert_has_changed()

    # ...but unused config can be changed without being rerun
    wait_beyond_mtime_resolution_atomicity()
    config3 = config2.copy()
    config3["unused"] += 1
    runner_config_unused_changed: Runner = runner_factory(rules=rules, config=config3)
    runner_config_unused_changed.run(resolved_target)
    assert_has_not_changed()

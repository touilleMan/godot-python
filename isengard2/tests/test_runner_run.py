import pytest
from pathlib import Path
import time

from .._runner import Runner

from .conftest import resolvify


def test_run_single_output(tmp_path: Path, runner_factory, rule_factory):
    target_path = tmp_path / "target.txt"
    resolved_target = resolvify(target_path)
    rules = [
        rule_factory(
            fn=lambda output, used: output.write_text(str(time.monotonic())),
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
        assert target_path.exists()
        nonlocal last_mtime, last_content
        new_ctime = target_path.stat().st_mtime
        new_content = target_path.read_text()
        assert new_ctime != last_mtime
        assert new_content != last_content
        last_mtime = new_ctime
        last_content = new_content

    def assert_has_not_changed():
        assert target_path.exists()
        assert target_path.stat().st_mtime == last_mtime
        assert target_path.read_text() == last_content

    # Run the rule
    runner.run(resolved_target)
    assert target_path.exists()
    last_mtime = target_path.stat().st_mtime
    last_content = target_path.read_text()

    time.sleep(0.01)  # Ensure time has changed enough !

    # Re-running should be a noop
    runner.run(resolved_target)
    assert_has_not_changed()

    time.sleep(0.01)  # Ensure time has changed enough !

    # If ctime has changed, rule should be rerun
    target_path.unlink()
    target_path.write_text(last_content)
    runner.run(resolved_target)
    assert_has_changed()

    time.sleep(0.01)  # Ensure time has changed enough !

    # If mtime has changed, rule should be rerun
    target_path.touch()
    runner.run(resolved_target)
    assert_has_changed()

    # If content has changed, of course rule should be rerun !
    target_path.write_text("dummy")
    runner.run(resolved_target)
    assert_has_changed()

    # Using another runner should not change anything
    other_runner: Runner = runner_factory(rules=rules, config=config)
    other_runner.run(resolved_target)
    assert_has_not_changed()

    # If config has changed, rule should be rerun...
    config2 = config.copy()
    config2["used"] += 1
    runner_config_changed: Runner = runner_factory(rules=rules, config=config2)
    runner_config_changed.run(resolved_target)
    assert_has_changed()

    # ...but unused config can be changed without being rerun
    config3 = config2.copy()
    config3["unused"] += 1
    runner_config_unused_changed: Runner = runner_factory(rules=rules, config=config3)
    runner_config_unused_changed.run(resolved_target)
    assert_has_not_changed()

import pytest
from pathlib import Path

from .._target import FileTargetHandler, TargetHandlersBundle
from .._exceptions import IsengardConsistencyError
from .._collector import Collector
from .._rule import Rule


@pytest.fixture
def collector():
    bundle = TargetHandlersBundle(target_handlers=[FileTargetHandler()])
    return Collector(target_handlers=bundle)


WORKDIR = Path("/foo/bar")


@pytest.fixture
def rule():
    return Rule(
        id="compile_x",
        fn=lambda output, inputs, cc, cflags: None,
        output="x.o#",
        inputs=["x.c#", "{gen_dir}/config.h#"],
        workdir=WORKDIR,
    )


@pytest.fixture
def config():
    return {"cc": "clang", "cflags": ("-O2", "-std=c99"), "gen_dir": "generated/"}



def test_ok(collector, rule, config):
    collector.add_rule(rule)
    config.pop("cflags")
    collector.add_lazy_config("cflags", lambda: None)
    collector.add_lazy_config("ldflags", lambda cflags, cc: None)

    def lazy_rule_gen(register_rule):
        @register_rule(output="foo.so", input="foo.o", id="linkstuff")
        def whatever(output, input, ldflags, cc):
            pass

    collector.add_lazy_rule(id="lazy_rule_gen", fn=lazy_rule_gen, workdir=WORKDIR)

    def lazy_rule_gen_multiple(register_rule, cc):
        assert cc == config["cc"]

        @register_rule(outputs=["foo.c", "foo_api.h"], inputs=["foo.pyx", "bar.pyi"])
        def generate_foo_c(outputs, inputs):
            pass

        @register_rule(outputs=["foo.o"], inputs=["foo.c"])
        def compile_foo_c(outputs, inputs, cc, cflags):
            pass

    collector.add_lazy_rule(id="lazy_rule_gen_multiple", fn=lazy_rule_gen_multiple, workdir=WORKDIR)

    resolved_rules = collector.configure(**config)
    assert resolved_rules.keys() == {
        'compile_x',
        'linkstuff',
        "lazy_rule_gen_multiple::generate_foo_c",
        "lazy_rule_gen_multiple::compile_foo_c",
    }

@pytest.mark.parametrize("kind", ["relative", "absolute"])
def test_resolve_target_relative_path(collector, rule, kind):
    if kind == "relative":
        outputs = ["{build_dir}/x.o#", "logs/compile.log#"]
        inputs = ["{gen_dir}/config.h#", "x.c#"]
        config = {"build_dir": Path("build"), "gen_dir": Path("gen/headers")}
        expected_resolved_outputs = ['/home/u/build/x.o#', '/home/u/logs/compile.log#']
        expected_resolved_inputs = ["/home/u/gen/headers/config.h#", "/home/u/x.c#"]
    else:
        assert kind == "absolute"
        outputs = ["{build_dir}/x.o#", "/logs/compile.log#"]
        inputs = ["{gen_dir}/config.h#", "/x.c#"]
        config = {"build_dir": Path("/build"), "gen_dir": Path("/gen/headers")}
        expected_resolved_outputs = ['/build/x.o#', '/logs/compile.log#']
        expected_resolved_inputs = ["/gen/headers/config.h#", "/x.c#"]

    rule = Rule(
        id="compile_x",
        fn=lambda outputs, inputs: None,
        outputs=outputs,
        inputs=inputs,
        workdir=Path("/home/u"),
    )
    collector.add_rule(rule)
    resolved_rules = collector.configure(**config)

    assert resolved_rules["compile_x"].resolved_outputs == expected_resolved_outputs
    assert resolved_rules["compile_x"].resolved_inputs == expected_resolved_inputs


@pytest.mark.parametrize("kind", ["same_rule", "same_id"])
def test_rule_duplication(collector, rule, config, kind):
    collector.add_rule(rule)

    if kind == "same_rule":
        collector.add_rule(rule)
    else:
        assert kind == "same_id"
        rule2 = Rule(
            id=rule.id,
            workdir=WORKDIR,
            fn=lambda output: None,
            output="whatever#",
        )
        collector.add_rule(rule2)

    with pytest.raises(IsengardConsistencyError):
        collector.configure(**config)


@pytest.mark.parametrize("kind", ["same_rule", "same_id"])
def test_lazy_rule_duplication(collector, kind):
    def genrule(register_rule):
        pass
    collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)

    if kind == "same_rule":
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)

    else:
        assert kind == "same_id"
        def genrule2(register_rule):
            pass
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_rule(id="genrule", fn=genrule2, workdir=WORKDIR)


def test_lazy_rule_same_fn_different_ids(collector):
    def genrule(register_rule):
        pass
    collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)
    collector.add_lazy_rule(id="genrule2", fn=genrule, workdir=WORKDIR)
    collector.configure()


@pytest.mark.parametrize("kind", ["same_rule", "same_id", "with_non_lazy_rule"])
def test_lazy_rule_generate_rule_duplication(collector, kind):
    def genrule(register_rule):
        @register_rule(output="foo")
        def my_rule(output):
            pass
    collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)

    if kind == "same_rule":
        collector.add_lazy_rule(id="genrule2", fn=genrule, workdir=WORKDIR)

    elif kind == "same_id":
        def genrule2(register_rule):
            @register_rule(output="foo", id="genrule::my_rule")
            def whatever(output):
                pass
        collector.add_lazy_rule(id="genrule2", fn=genrule2, workdir=WORKDIR)

    else:
        assert kind == "with_non_lazy_rule"
        rule2 = Rule(
            id="genrule::my_rule",
            workdir=WORKDIR,
            fn=lambda output: None,
            output="whatever#",
        )
        collector.add_rule(rule2)

    with pytest.raises(IsengardConsistencyError):
        collector.configure()


def test_lazy_rule_missing_register_rule_param(collector):
    def genrule():
        pass

    collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)

    with pytest.raises(IsengardConsistencyError):
        collector.configure()


@pytest.mark.parametrize("kind", ["same_fn", "same_id"])
def test_lazy_config_duplication(collector, kind):
    def genconfig():
        pass

    collector.add_lazy_config("genconfig", genconfig)

    if kind == "same_fn":
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_config("genconfig", genconfig)
    elif kind == "same_id":
        def genconfig2():
            pass
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_config("genconfig", genconfig2)



def test_lazy_config_duplication_with_regular_config(collector):
    def foo():
        pass

    collector.add_lazy_config("foo", foo)

    with pytest.raises(IsengardConsistencyError):
        collector.configure(foo=42)


def test_missing_config(collector, rule, config):
    collector.add_rule(rule)

    config.pop("cc")

    with pytest.raises(IsengardConsistencyError):
        collector.configure(**config)
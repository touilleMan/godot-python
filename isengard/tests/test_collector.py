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
    return {
        "cc": "clang",
        "cflags": ("-O2", "-std=c99"),
        "gen_dir": "generated/",
        "host_platform": "linux-x86",
    }


def test_ok(collector, rule, config):
    collector.add_rule(rule)
    config.pop("cflags")
    collector.add_lazy_config("cflags", lambda: None)
    collector.add_lazy_config("ldflags", lambda cflags, cc: None)

    def lazy_rule_gen(register_rule):
        @register_rule(output="foo.so#", input="foo.o#", id="linkstuff")
        def whatever(output, input, ldflags, cc):
            pass

    collector.add_lazy_rule(id="lazy_rule_gen", fn=lazy_rule_gen, workdir=WORKDIR)

    def lazy_rule_gen_multiple(register_rule, cc, host_platform):
        assert cc == config["cc"]

        @register_rule(outputs=["foo.c#", "foo_api.h#"], inputs=["foo.pyx#", "bar.pyi#"])
        def generate_foo_c(outputs, inputs):
            pass

        @register_rule(outputs=["foo.o#"], inputs=["foo.c#"])
        def compile_foo_c(outputs, inputs, cc, cflags):
            pass

    collector.add_lazy_rule(id="lazy_rule_gen_multiple", fn=lazy_rule_gen_multiple, workdir=WORKDIR)

    configured_rules, configured_config = collector.configure(**config)
    assert configured_rules.keys() == {
        "compile_x",
        "linkstuff",
        "lazy_rule_gen_multiple::generate_foo_c",
        "lazy_rule_gen_multiple::compile_foo_c",
    }
    assert configured_config.keys() == {"cc", "gen_dir", "host_platform", "cflags", "ldflags"}
    # Ensure lazy rules also contains their generator config dependencies
    assert configured_rules["lazy_rule_gen_multiple::generate_foo_c"].needed_config == {
        "cc",
        "host_platform",
    }
    assert configured_rules["lazy_rule_gen_multiple::compile_foo_c"].needed_config == {
        "cc",
        "cflags",
        "host_platform",
    }


@pytest.mark.parametrize("kind", ["relative", "absolute"])
def test_configure_target_relative_path(collector, rule, kind):
    if kind == "relative":
        outputs = ["{build_dir}/x.o#", "logs/compile.log#"]
        inputs = ["{gen_dir}/config.h#", "x.c#"]
        config = {"build_dir": Path("build"), "gen_dir": Path("gen/headers")}
        expected_configured_outputs = ["/home/u/build/x.o#", "/home/u/logs/compile.log#"]
        expected_configured_inputs = ["/home/u/gen/headers/config.h#", "/home/u/x.c#"]
    else:
        assert kind == "absolute"
        outputs = ["{build_dir}/x.o#", "/logs/compile.log#"]
        inputs = ["{gen_dir}/config.h#", "/x.c#"]
        config = {"build_dir": Path("/build"), "gen_dir": Path("/gen/headers")}
        expected_configured_outputs = ["/build/x.o#", "/logs/compile.log#"]
        expected_configured_inputs = ["/gen/headers/config.h#", "/x.c#"]

    rule = Rule(
        id="compile_x",
        fn=lambda outputs, inputs: None,
        outputs=outputs,
        inputs=inputs,
        workdir=Path("/home/u"),
    )
    collector.add_rule(rule)
    configured_rules, _ = collector.configure(**config)

    assert configured_rules["compile_x"].configured_outputs == expected_configured_outputs
    assert configured_rules["compile_x"].configured_inputs == expected_configured_inputs


@pytest.mark.parametrize("kind", ["same_rule", "same_id"])
def test_rule_duplication(collector, rule, config, kind):
    collector.add_rule(rule)

    if kind == "same_rule":
        collector.add_rule(rule)
        expected_err = "Multiple rules to produce `x.o#`: `compile_x` and `compile_x`"
    else:
        assert kind == "same_id"
        expected_err = r"Multiple rules have the same ID `compile_x`: <ConfiguredRule id=compile_x .*> and <ConfiguredRule id=compile_x .*>"
        rule2 = Rule(
            id=rule.id,
            workdir=WORKDIR,
            fn=lambda output: None,
            output="whatever#",
        )
        collector.add_rule(rule2)

    with pytest.raises(IsengardConsistencyError, match=expected_err):
        collector.configure(**config)


@pytest.mark.parametrize("kind", ["same_rule", "same_id"])
def test_lazy_rule_duplication(collector, kind):
    def genrule(register_rule):
        pass

    collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)

    if kind == "same_rule":
        expected_err = r"Multiple lazy rules have the same ID `genrule`: genrule and <function"
        with pytest.raises(IsengardConsistencyError, match=expected_err):
            collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)

    else:
        assert kind == "same_id"

        def genrule2(register_rule):
            pass

        expected_err = r"Multiple lazy rules have the same ID `genrule`: genrule and <function"
        with pytest.raises(IsengardConsistencyError, match=expected_err):
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

    expected_err = r"Lazy rule `genrule` is missing mandatory `register_rule` parameter"
    with pytest.raises(IsengardConsistencyError, match=expected_err):
        collector.add_lazy_rule(id="genrule", fn=genrule, workdir=WORKDIR)


@pytest.mark.parametrize("kind", ["same_fn", "same_id"])
def test_lazy_config_duplication(collector, kind):
    def genconfig():
        pass

    collector.add_lazy_config("genconfig", genconfig)

    if kind == "same_fn":
        expected_err = r"Multiple lazy rules have the same ID `genconfig`: genconfig and <function"
        with pytest.raises(IsengardConsistencyError, match=expected_err):
            collector.add_lazy_config("genconfig", genconfig)
    elif kind == "same_id":

        def genconfig2():
            pass

        expected_err = r"Multiple lazy rules have the same ID `genconfig`: genconfig and <function"
        with pytest.raises(IsengardConsistencyError, match=expected_err):
            collector.add_lazy_config("genconfig", genconfig2)


def test_lazy_config_duplication_with_regular_config(collector):
    def foo():
        pass

    collector.add_lazy_config("foo", foo)

    expected_err = r"Config `foo` is defined multiple times: <function .*> and 42"
    with pytest.raises(IsengardConsistencyError, match=expected_err):
        collector.configure(foo=42)


def test_lazy_config_with_kwargs(collector):
    def foo(**kwargs):
        return kwargs["bar"] * 2

    collector.add_lazy_config("foo", foo, kwargs_params={"bar"})
    _, config = collector.configure(bar=21)
    assert config == {"bar": 21, "foo": 42}


def test_lazy_rule_with_kwargs(collector):
    def genrule(register_rule, **kwargs):
        @register_rule(id=kwargs["generated_id"], output=kwargs["generated_output"])
        def fn(output):
            pass

    collector.add_lazy_rule(
        id="genrule",
        fn=genrule,
        workdir=WORKDIR,
        kwargs_params={"generated_id", "generated_output"},
    )
    rules, _ = collector.configure(generated_id="generated42", generated_output="generated?")
    assert rules["generated42"].outputs == ["generated?"]


def test_missing_config(collector, rule, config):
    collector.add_rule(rule)

    config.pop("cc")

    expected_err = r"Rule `compile_x` contains unknown config item\(s\) `cc`"
    with pytest.raises(IsengardConsistencyError, match=expected_err):
        collector.configure(**config)

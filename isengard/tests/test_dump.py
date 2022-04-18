import pytest
from pathlib import Path

from .._dump import dump_graph
from .._rule import ConfiguredRule
from .._target import ConfiguredTargetID
from .._exceptions import IsengardRunError


def rule_factory(id, outputs, inputs, params, configured_outputs=None, configured_inputs=None):
    return ConfiguredRule(
        id=id,
        fn=lambda: None,  # Bad params, but this is not checked here
        params=params,
        outputs=outputs,
        inputs=inputs,
        configured_outputs=configured_outputs or [f"/foo/bar/{x}" for x in outputs],
        configured_inputs=configured_inputs or [f"/foo/bar/{x}" for x in inputs],
        workdir=Path("/foo/bar"),
    )


@pytest.fixture
def rules():
    return [
        rule_factory(
            id="generate_config_header",
            outputs=["{gen_dir}/config.h#"],
            configured_outputs=["/foo/bar/generated/config.h#"],
            inputs=[],
            params={"host_platform"},
        ),
        rule_factory(
            id="compile_x",
            outputs=["x.o#"],
            inputs=["x.c#", "{gen_dir}/config.h#"],
            configured_inputs=["/foo/bar/x.c#", "/foo/bar/generated/config.h#"],
            params={"cc", "cflags"},
        ),
        rule_factory(
            id="compile_y",
            outputs=["y.o#"],
            inputs=["y.c#", "{gen_dir}/config.h#"],
            configured_inputs=["/foo/bar/y.c#", "/foo/bar/generated/config.h#"],
            params={"cc", "cflags"},
        ),
        rule_factory(
            id="compile_z",
            outputs=["z.o#"],
            inputs=["z.c#", "{gen_dir}/config.h#"],
            configured_inputs=["/foo/bar/z.c#", "/foo/bar/generated/config.h#"],
            params={"cc", "cflags"},
        ),
        rule_factory(
            id="link_xyz",
            outputs=["xyz.so#", "xyz.a#"],
            inputs=["x.o#", "y.o#", "z.o#"],
            params={"cc", "linkflags"},
        ),
        rule_factory(
            id="compile_main",
            outputs=["main.o#"],
            inputs=["main.c#"],
            params={"cc", "cflags"},
        ),
        rule_factory(
            id="link_aout",
            outputs=["a.out#"],
            inputs=["xyz.so#", "main.o#"],
            params={"cc", "linkflags"},
        ),
    ]


def test_empty():
    graph = dump_graph(
        rules=[],
    )

    assert graph == ""


@pytest.mark.parametrize("kind", ("bad_discriminant", "bad_target"))
def test_unknown_target(rules, kind):
    if kind == "bad_discriminant":
        target_filter = ConfiguredTargetID("dummy")
    else:
        assert kind == "bad_target"
        target_filter = ConfiguredTargetID("dummy#")

    expected_err = r"No rule has target `dummy#?` as output !"
    with pytest.raises(IsengardRunError, match=expected_err):
        dump_graph(rules, target_filter=target_filter)


def test_single_target(rules):
    assert dump_graph(rules, target_filter=ConfiguredTargetID("/foo/bar/x.o#")) == (
        "x.o#\n"
        "├──rule:compile_x\n"
        "├──configs:cc, cflags\n"
        "├─x.c#\n"
        "└─{gen_dir}/config.h#\n"
        "  ├──rule:generate_config_header\n"
        "  └──configs:host_platform\n"
    )


@pytest.mark.parametrize("display_configured", (False, True))
def test_full(rules, display_configured):
    gen_prefix = "/foo/bar/generated/" if display_configured else "{gen_dir}/"
    prefix = "/foo/bar/" if display_configured else ""
    assert dump_graph(rules, display_configured=display_configured) == (
        "{prefix}a.out#\n"
        "├──rule:link_aout\n"
        "├──configs:cc, linkflags\n"
        "├─{prefix}xyz.so#\n"
        "│ ├──rule:link_xyz\n"
        "│ ├──configs:cc, linkflags\n"
        "│ ├─{prefix}x.o#\n"
        "│ │ ├──rule:compile_x\n"
        "│ │ ├──configs:cc, cflags\n"
        "│ │ ├─{prefix}x.c#\n"
        "│ │ └─{gen_prefix}config.h#\n"
        "│ │   ├──rule:generate_config_header\n"
        "│ │   └──configs:host_platform\n"
        "│ ├─{prefix}y.o#\n"
        "│ │ ├──rule:compile_y\n"
        "│ │ ├──configs:cc, cflags\n"
        "│ │ ├─{prefix}y.c#\n"
        "│ │ └─{gen_prefix}config.h#\n"
        "│ │   ├──rule:generate_config_header\n"
        "│ │   └─…\n"
        "│ └─{prefix}z.o#\n"
        "│   ├──rule:compile_z\n"
        "│   ├──configs:cc, cflags\n"
        "│   ├─{prefix}z.c#\n"
        "│   └─{gen_prefix}config.h#\n"
        "│     ├──rule:generate_config_header\n"
        "│     └─…\n"
        "└─{prefix}main.o#\n"
        "  ├──rule:compile_main\n"
        "  ├──configs:cc, cflags\n"
        "  └─{prefix}main.c#\n"
        "{prefix}xyz.a#\n"
        "├──rule:link_xyz\n"
        "└─…\n"
    ).format(prefix=prefix, gen_prefix=gen_prefix)

import pytest
from pathlib import Path

import isengard


@pytest.fixture
def isg(tmp_path):
    return isengard.Isengard(
        self_file=tmp_path / "build.py", db=tmp_path / ".isengard.sqlite"
    )


def test_rule(isg):
    @isg.rule(output="x.o", input="x.c")
    def compile_c(output, input):
        pass

    assert len(isg._rules) == 1
    isg.configure()

    assert isg.dump_graph() == ("x.o#\n" "├──rule:compile_c\n" "└─x.c#\n")

    # Ensure idempotency
    assert isg.dump_graph() == ("x.o#\n" "├──rule:compile_c\n" "└─x.c#\n")


def test_graph_on_nested_rule(isg):
    @isg.lazy_config
    def cc(host_platform):
        pass

    @isg.rule(output="config.h")
    def generate_config_header(output, host_platform):
        pass

    @isg.rule(output="x.o", inputs=["x.c", "config.h"])
    def compile_x(output, inputs, cc, cflags):
        pass

    @isg.rule(output="y.o", inputs=["y.c", "config.h"])
    def compile_y(output, inputs, cc, cflags):
        pass

    @isg.rule(output="z.o", inputs=["z.c", "config.h"])
    def compile_z(output, inputs, cc, cflags):
        pass

    @isg.rule(outputs=["xyz.so", "xyz.a"], inputs=["x.o", "y.o", "z.o"])
    def link_xyz(outputs, inputs, cc, linkflags):
        pass

    @isg.rule(output="main.o", input="main.c")
    def compile_main(output, input, cc, cflags):
        pass

    @isg.rule(outputs=["a.out"], inputs=["xyz.so", "main.o"])
    def link_aout(outputs, inputs, cc, linkflags):
        pass

    isg.configure(host_platform="", cflags="", linkflags="")

    assert isg.dump_graph() == (
        "a.out#\n"
        "├──rule:link_aout\n"
        "├──config:cc\n"
        "├──config:linkflags\n"
        "├─xyz.so#\n"
        "│ ├──rule:link_xyz\n"
        "│ ├──config:cc\n"
        "│ ├──config:linkflags\n"
        "│ ├─x.o#\n"
        "│ │ ├──rule:compile_x\n"
        "│ │ ├──config:cc\n"
        "│ │ ├──config:cflags\n"
        "│ │ ├─x.c#\n"
        "│ │ └─config.h#\n"
        "│ │   ├──rule:generate_config_header\n"
        "│ │   └──config:host_platform\n"
        "│ ├─y.o#\n"
        "│ │ ├──rule:compile_y\n"
        "│ │ ├──config:cc\n"
        "│ │ ├──config:cflags\n"
        "│ │ ├─y.c#\n"
        "│ │ └─config.h#\n"
        "│ │   ├──rule:generate_config_header\n"
        "│ │   └─…\n"
        "│ └─z.o#\n"
        "│   ├──rule:compile_z\n"
        "│   ├──config:cc\n"
        "│   ├──config:cflags\n"
        "│   ├─z.c#\n"
        "│   └─config.h#\n"
        "│     ├──rule:generate_config_header\n"
        "│     └─…\n"
        "└─main.o#\n"
        "  ├──rule:compile_main\n"
        "  ├──config:cc\n"
        "  ├──config:cflags\n"
        "  └─main.c#\n"
        "xyz.a#\n"
        "├──rule:link_xyz\n"
        "└─…\n"
    )


def test_rule_missing_config(isg):
    @isg.rule(output="x.o", input="x.c")
    def compile_c(output, input, missing):
        pass

    assert isg.dump_graph() == (
        "x.o#\n" "├──rule:compile_c\n" "├──config:missing\n" "└─x.c#\n"
    )

    with pytest.raises(isengard.IsengardConsistencyError):
        isg.configure()


def test_rule_mismatch_input_output_params(isg):
    with pytest.raises(TypeError):

        @isg.rule(output="x.o", input="x.c")
        def compile_c(output, inputs):
            pass

    with pytest.raises(TypeError):

        @isg.rule(output="x.o", inputs=["x.c"])
        def compile_c(output, input):
            pass

    with pytest.raises(TypeError):

        @isg.rule(output="x.o", input="x.c")
        def compile_c(outputs, input):
            pass

    with pytest.raises(TypeError):

        @isg.rule(outputs=["x.o"], inputs=["x.c"])
        def compile_c(output, input):
            pass

    isg.configure()
    # Invalid rules should have been ignored
    assert isg.dump_graph() == ""

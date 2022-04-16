import pytest
from typing import Union
from pathlib import Path

from .._api import Isengard
from .._target import FileTargetHandler, FolderTargetHandler
from .._exceptions import IsengardUnknownTargetError


class IsengardForTest(Isengard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.test_events = []


@pytest.fixture
def isg(memory_sqlite3, tmp_path):
    isg = IsengardForTest(self_file=tmp_path / "build.py")

    def _clean_path(path):
        return path.relative_to(tmp_path).as_posix()

    @isg.lazy_config
    def cc(host_platform):
        isg.test_events.append("define cc")
        return f"cc-{host_platform}"

    @isg.lazy_config
    def buildir(rootdir, host_platform):
        buildir_path = rootdir / f"build-{host_platform}"
        isg.test_events.append("define buildir")
        return buildir_path

    @isg.rule(output="{buildir}/includes/config.h")
    def genarate_config_header(output):
        isg.test_events.append(f"generate {_clean_path(output)}")

    @isg.rule(
        output="{buildir}/x.o",
        inputs=["x.c", "{buildir}/includes/config.h"],
        id="compile_x",
    )
    @isg.rule(
        output="{buildir}/y.o",
        inputs=["y.c", "{buildir}/includes/config.h"],
        id="compile_y",
    )
    def compile(output, inputs, cc, cflags):
        cmd = f"{cc} {cflags} -o {_clean_path(output)}"
        for input in inputs:
            if input.name.endswith(".c"):
                cmd += f" {_clean_path(input)}"
            elif input.name.endswith(".h"):
                cmd += f" -I {_clean_path(input.parent)}"
        isg.test_events.append(cmd)

    @isg.rule(output="{buildir}/a.out", inputs=["{buildir}/x.o", "{buildir}/y.o"])
    def link_aout(output, inputs, cc, linkflags):
        inputs = sorted(str(_clean_path(input)) for input in inputs)
        isg.test_events.append(f"{cc} {linkflags} -o {_clean_path(output)} {' '.join(inputs)}")

    @isg.rule(output="tests@", input="{buildir}/a.out")
    def run_tests(output, input):
        isg.test_events.append("run tests")

    @isg.lazy_rule
    def lazy_generate_distdir(host_platform, register_rule):
        isg.test_events.append("define generate_distdir")

        @register_rule(output="distdir?", input="{buildir}/a.out")
        def generate_distdir(output, input, buildir):
            output_path = buildir / f"foobar-{host_platform}"
            isg.test_events.append(f"cp {_clean_path(input)} {_clean_path(output_path)}")
            output.resolve(output_path, FolderTargetHandler())

    @isg.rule(output="distzip?", input="distdir?")
    def generate_distzip(output, input):
        input_path, _ = input.resolved
        output_path = input_path.parent / f"{input_path.name}.tar.bz2"
        isg.test_events.append(f"tar -cjf {_clean_path(output_path)} {_clean_path(input_path)}")
        output.resolve(output_path, FileTargetHandler())

    isg.configure(
        cflags="--std=c99 -O2",
        linkflags="--std=c99",
        host_platform="x86",
    )

    return isg


@pytest.mark.parametrize(
    "run_arg",
    [
        "build-x86/dummy#",
        "build-x86/../build-x86/a.out#",  # no path resolution for str
        Path("build-x86/dummy"),  # Relative path leading to the wrong absolute path
        Path("{buildir}/a.out"),  # Path should not have bracket replaced
    ],
)
def test_run_bad_target(isg: IsengardForTest, run_arg: Union[str, Path]):
    expected_err = r"^No rule has target `.*#` as output$"
    with pytest.raises(IsengardUnknownTargetError, match=expected_err):
        isg.run(run_arg)


@pytest.mark.parametrize(
    "run_arg",
    [
        "{buildir}/a.out#",
        "{buildir}/a.out",  # `#` is the default handler, so can omit it
        "build-x86/a.out#",
        Path("build-x86/a.out"),
        Path("build-x86/foo/../a.out"),
    ],
)
def test_run_success(isg: IsengardForTest, run_arg: Union[str, Path]):
    print(isg.dump_graph())
    isg.run(run_arg)

    assert isg.test_events == [
        "define cc",
        "define buildir",
        "define generate_distdir",
        "generate build-x86/includes/config.h",
        "cc-x86 --std=c99 -O2 -o build-x86/x.o x.c -I build-x86/includes",
        "cc-x86 --std=c99 -O2 -o build-x86/y.o y.c -I build-x86/includes",
        "cc-x86 --std=c99 -o build-x86/a.out build-x86/x.o build-x86/y.o",
    ]


def test_run_deferred_target(isg: IsengardForTest):
    isg.run("distzip?")

    assert isg.test_events == [
        "define cc",
        "define buildir",
        "define generate_distdir",
        "generate build-x86/includes/config.h",
        "cc-x86 --std=c99 -O2 -o build-x86/x.o x.c -I build-x86/includes",
        "cc-x86 --std=c99 -O2 -o build-x86/y.o y.c -I build-x86/includes",
        "cc-x86 --std=c99 -o build-x86/a.out build-x86/x.o build-x86/y.o",
        "cp build-x86/a.out build-x86/foobar-x86",
        "tar -cjf build-x86/foobar-x86.tar.bz2 build-x86/foobar-x86",
    ]


def test_run_virtual_target(isg: IsengardForTest):
    isg.run("tests@")

    assert isg.test_events == [
        "define cc",
        "define buildir",
        "define generate_distdir",
        "generate build-x86/includes/config.h",
        "cc-x86 --std=c99 -O2 -o build-x86/x.o x.c -I build-x86/includes",
        "cc-x86 --std=c99 -O2 -o build-x86/y.o y.c -I build-x86/includes",
        "cc-x86 --std=c99 -o build-x86/a.out build-x86/x.o build-x86/y.o",
        "run tests",
    ]


def test_dump_graph(isg: IsengardForTest):
    assert isg.dump_graph() == (
        "tests@\n"
        "├──rule:run_tests\n"
        "└─{buildir}/a.out\n"
        "  ├──rule:link_aout\n"
        "  ├──configs:cc, linkflags\n"
        "  ├─{buildir}/x.o\n"
        "  │ ├──rule:compile_x\n"
        "  │ ├──configs:cc, cflags\n"
        "  │ ├─x.c\n"
        "  │ └─{buildir}/includes/config.h\n"
        "  │   └──rule:genarate_config_header\n"
        "  └─{buildir}/y.o\n"
        "    ├──rule:compile_y\n"
        "    ├──configs:cc, cflags\n"
        "    ├─y.c\n"
        "    └─{buildir}/includes/config.h\n"
        "      ├──rule:genarate_config_header\n"
        "      └─…\n"
        "distzip?\n"
        "├──rule:generate_distzip\n"
        "└─distdir?\n"
        "  ├──rule:lazy_generate_distdir::generate_distdir\n"
        "  ├──configs:buildir, host_platform\n"
        "  └─{buildir}/a.out\n"
        "    ├──rule:link_aout\n"
        "    └─…\n"
    )

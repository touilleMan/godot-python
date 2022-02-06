import pytest
from pathlib import Path

from isengard import Isengard, IsengardConsistencyError


@pytest.fixture
def isg(tmp_path):
    isg = Isengard(self_file=tmp_path / "build.py", db=tmp_path / ".isengard.sqlite")
    isg.test_events = []

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
        name="compile_x",
    )
    @isg.rule(
        output="{buildir}/y.o",
        inputs=["y.c", "{buildir}/includes/config.h"],
        name="compile_y",
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

    @isg.rule(output="distdir@", input="{buildir}/a.out")
    def generate_distdir(output, input, buildir, host_platform):
        output_path = buildir / f"foobar-{host_platform}"
        isg.test_events.append(f"cp {_clean_path(input)} {_clean_path(output_path)}")
        output.resolve(output_path)

    @isg.rule(output="distzip@", input="distdir@")
    def generate_distdir(output, input, buildir):
        output_path = input.parent / f"{input.name}.tar.bz2"
        isg.test_events.append(f"tar -cjf {_clean_path(output_path)} {_clean_path(input)}")
        output.resolve(output_path)

    isg.configure(
        cflags="--std=c99 -O2",
        linkflags="--std=c99",
        host_platform="x86",
    )

    return isg


@pytest.mark.parametrize(
    "run_arg",
    [
        "build-x86/dummy",
        Path("build-x86/dummy"),  # Relative path leading to the wrong absolute path
        Path("{buildir}/a.out"),  # Path should not have bracket replaced
    ],
)
def test_run_bad_target(isg, run_arg):
    with pytest.raises(IsengardConsistencyError):
        isg.run(run_arg)


@pytest.mark.parametrize(
    "run_arg",
    [
        "{buildir}/a.out",
        "build-x86/a.out",
        "build-x86/foo/../a.out",
        Path("build-x86/a.out"),
    ],
)
def test_run_success(isg, run_arg):
    print(isg.dump_graph())
    isg.run(run_arg)

    assert isg.test_events == [
        "define cc",
        "define buildir",
        "generate build-x86/includes/config.h",
        "cc-x86 --std=c99 -O2 -o build-x86/x.o x.c -I build-x86/includes",
        "cc-x86 --std=c99 -O2 -o build-x86/y.o y.c -I build-x86/includes",
        "cc-x86 --std=c99 -o build-x86/a.out build-x86/x.o build-x86/y.o",
    ]


def test_run_virtual_target(isg):
    isg.run("distzip@")

    assert isg.test_events == [
        "define cc",
        "define buildir",
        "generate build-x86/includes/config.h",
        "cc-x86 --std=c99 -O2 -o build-x86/x.o x.c -I build-x86/includes",
        "cc-x86 --std=c99 -O2 -o build-x86/y.o y.c -I build-x86/includes",
        "cc-x86 --std=c99 -o build-x86/a.out build-x86/x.o build-x86/y.o",
        "cp build-x86/a.out build-x86/foobar-x86",
        "tar -cjf build-x86/foobar-x86.tar.bz2 build-x86/foobar-x86",
    ]

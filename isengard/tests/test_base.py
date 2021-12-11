# import pytest
# from pathlib import Path

# import isengard


# @pytest.fixture
# def isg(tmp_path):
#     isg = isengard.Isengard(self_file=tmp_path / "build.py", db=tmp_path / ".isengard.sqlite")
#     isg.events = []

#     @isg.rule(output="foo.o", input="foo.c")
#     def build_c(output: Path, input: Path, basedir: Path):
#         isg.events.append(f"cc -c {input.relative_to(basedir)} -o {output.relative_to(basedir)}")
#         output.touch()

#     (tmp_path / "foo.c").touch()
#     (tmp_path / "build.py").touch()
#     return isg


# def test_run_before_configure(isg):
#     with pytest.raises(RuntimeError):
#         isg.run("foo.o")


# def test_run_unknown_target(isg):
#     with pytest.raises(RuntimeError):
#         isg.configure()
#         isg.run("dummy.txt")


# def test_single_run(isg):
#     isg.configure()
#     isg.run("foo.o")

#     assert isg.events == ["cc -c foo.c -o foo.o"]


# @pytest.mark.xfail(reason="not implemented yet")
# def test_idempotent_run(isg):
#     isg.configure()
#     isg.run("foo.o")
#     isg.run("foo.o")

#     assert isg.events == ["cc -c foo.c -o foo.o"]


# def test_clean(isg):
#     isg.clean("foo.o")
#     isg.clean("foo.o")


# def test_idempotent_clean(isg):
#     isg.clean("foo.o")
#     isg.clean("foo.o")

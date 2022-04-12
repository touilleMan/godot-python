# import pytest

# from .._exceptions import IsengardUnknownTargetError, IsengardConsistencyError
# from .._runner import Runner
# from .._target import TargetHandlersBundle, FileTargetHandler, ResolvedTargetID
# from .._rule import Rule, ResolvedRule
# from .._collector import Collector


# @pytest.fixture
# def rule_factory(tmp_path):
#     default_workdir = tmp_path / "workdir"
#     default_workdir.mkdir()

#     def _rule_factory(id, fn, outputs, inputs, params, resolved_outputs=None, resolved_inputs=None, workdir=default_workdir):
#         return ResolvedRule(
#             id=id,
#             fn=fn,
#             params=params,
#             outputs=outputs,
#             inputs=inputs,
#             resolved_outputs=resolved_outputs or [f"{workdir}/{x}" for x in outputs],
#             resolved_inputs=resolved_inputs or [f"{workdir}/{x}" for x in inputs],
#             workdir=workdir,
#         )
#     return _rule_factory


# def rule_factory(id, fn, outputs, inputs, params, resolved_outputs=None, resolved_inputs=None, workdir=default_workdir):
#     return ResolvedRule(
#         id=id,
#         fn=fn,
#         params=params,
#         outputs=outputs,
#         inputs=inputs,
#         resolved_outputs=resolved_outputs or [f"{workdir}/{x}" for x in outputs],
#         resolved_inputs=resolved_inputs or [f"{workdir}/{x}" for x in inputs],
#         workdir=workdir,
#     )


# @pytest.fixture
# def rules():
#     return [
#         rule_factory(
#             id="generate_config_header",
#             outputs=["{gen_dir}/config.h#"],
#             resolved_outputs=["/foo/bar/generated/config.h#"],
#             inputs=[],
#             params={"host_platform"},
#         ),
#         rule_factory(
#             id="compile_x",
#             outputs=["x.o#"],
#             inputs=["x.c#", "{gen_dir}/config.h#"],
#             resolved_inputs=["/foo/bar/x.c#", "/foo/bar/generated/config.h#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="compile_y",
#             outputs=["y.o#"],
#             inputs=["y.c#", "{gen_dir}/config.h#"],
#             resolved_inputs=["/foo/bar/y.c#", "/foo/bar/generated/config.h#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="compile_z",
#             outputs=["z.o#"],
#             inputs=["z.c#", "{gen_dir}/config.h#"],
#             resolved_inputs=["/foo/bar/z.c#", "/foo/bar/generated/config.h#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="link_xyz",
#             outputs=["xyz.so#", "xyz.a#"],
#             inputs=["x.o#", "y.o#", "z.o#"],
#             params={"cc", "linkflags"},
#         ),
#         rule_factory(
#             id="compile_main",
#             outputs=["main.o#"],
#             inputs=["main.c#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="link_aout",
#             outputs=["a.out#"],
#             inputs=["xyz.so#", "main.o#"],
#             params={"cc", "linkflags"},
#         ),
#     ]


# def rule_factory(id, fn, outputs, inputs, params, resolved_outputs=None, resolved_inputs=None, workdir=None):
#     return ResolvedRule(
#         id=id,
#         fn=fn,
#         params=params,
#         outputs=outputs,
#         inputs=inputs,
#         resolved_outputs=resolved_outputs or outputs,
#         resolved_inputs=resolved_inputs or inputs,
#         workdir=workdir or Path("/foo/bar"),
#     )


# @pytest.fixture
# def rules():
#     return [
#         rule_factory(
#             id="generate_config_header",
#             outputs=["{gen_dir}/config.h#"],
#             resolved_outputs=["generated/config.h#"],
#             inputs=[],
#             params={"host_platform"},
#         ),
#         rule_factory(
#             id="compile_x",
#             outputs=["x.o#"],
#             inputs=["x.c#", "{gen_dir}/config.h#"],
#             resolved_inputs=["x.c#", "generated/config.h#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="compile_y",
#             outputs=["y.o#"],
#             inputs=["y.c#", "{gen_dir}/config.h#"],
#             resolved_inputs=["y.c#", "generated/config.h#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="compile_z",
#             outputs=["z.o#"],
#             inputs=["z.c#", "{gen_dir}/config.h#"],
#             resolved_inputs=["z.c#", "generated/config.h#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="link_xyz",
#             outputs=["xyz.so#", "xyz.a#"],
#             inputs=["x.o#", "y.o#", "z.o#"],
#             params={"cc", "linkflags"},
#         ),
#         rule_factory(
#             id="compile_main",
#             outputs=["main.o#"],
#             inputs=["main.c#"],
#             params={"cc", "cflags"},
#         ),
#         rule_factory(
#             id="link_aout",
#             outputs=["a.out#"],
#             inputs=["xyz.so#", "main.o#"],
#             params={"cc", "linkflags"},
#         ),
#     ]


# @pytest.fixture
# def target_handlers_bundle():
#     file_handler = FileTargetHandler()
#     return TargetHandlersBundle(
#         target_handlers=[file_handler],
#     )


# def test_base(tmp_path, target_handlers_bundle, rules):
#     db_path = tmp_path / "db.sqlite"
#     config = {}

#     run_factory("")

#     runner = Runner(
#         rules={r.id: r for r in rules},
#         config=config,
#         target_handlers=target_handlers_bundle,
#         db_path=db_path,
#     )


# def test_run_unknown_target(runner: Runner):
#     with pytest.raises(IsengardUnknownTargetError):
#         runner.run(ResolvedTargetID("dummy"))


# def test_clean_unknown_target(runner: Runner):
#     with pytest.raises(IsengardUnknownTargetError):
#         runner.clean(ResolvedTargetID("dummy"))


# def rule_factory(id, fn=None, outputs=None, inputs=None):
#     if not fn:
#         def fn(outputs, inputs):
#             for output in outputs:
#                 output.touch()

#     return ResolvedRule(
#         id=id,
#         fn=fn,
#         params=params,
#         outputs=outputs,
#         inputs=inputs,
#         resolved_outputs=resolved_outputs or [f"{workdir}/{x}" for x in outputs],
#         resolved_inputs=resolved_inputs or [f"{workdir}/{x}" for x in inputs],
#         workdir=workdir,
#     )

# @pytest.fixture
# def runner_with_recursive_rules(tmp_path, target_handlers_bundle):
#     db_path = tmp_path / "db.sqlite"
#     rules = [
#         rule_factory(
#             id="rule_a_from_b",
#             outputs=["a#"],
#             inputs="b#",
#             workdir=tmp_path,
#         ),
#         rule_factory(
#             id="rule_b_from_c",
#             outputs=["b#"],
#             inputs="c#",
#             workdir=tmp_path,
#         ),
#         rule_factory(
#             id="rule_c_from_a",
#             outputs=["c#"],
#             inputs="a#",
#             workdir=tmp_path,
#         ),
#     ]
#     return Runner(
#         rules={r.id: r for r in rules},
#         config={},
#         target_handlers=target_handlers_bundle,
#         db_path=db_path,
#     )


# def test_run_recursive_rules(runner_with_recursive_rules: Runner):
#     with pytest.raises(IsengardConsistencyError):
#         runner_with_recursive_rules.run(ResolvedTargetID("dummy"))


# def test_clean_recursive_rules(runner_with_recursive_rules: Runner):
#     with pytest.raises(IsengardConsistencyError):
#         runner_with_recursive_rules.clean(ResolvedTargetID("dummy"))

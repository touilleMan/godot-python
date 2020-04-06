import os
from uuid import uuid4
from SCons.Node.FS import File
from SCons.Action import Action
from SCons.Defaults import Delete
from SCons.Util import is_List
from SCons.Errors import UserError


def install_marker(target):
    with open(target.abspath, "w") as fd:
        fd.write(
            "Dummy file to represent the completion of a virtual action.\n"
            "Modifying or removing this file will force rebuild.\n"
            "\n"
            f"Unique hash: {uuid4().hex}\n"
        )


def virtual_target_command(env, marker, condition, source, action):
    if not isinstance(marker, File):
        raise UserError("`marker` must be a File")

    if not condition(env) and os.path.exists(marker.abspath):
        # Condition has changed in our back, force rebuild
        env.Execute(Delete(marker))

    return env.Command(
        marker,
        source,
        [
            *(action if is_List(action) else [action]),
            Action(
                lambda target, source, env: install_marker(target[0]),
                "Write $TARGET to mark task complete",
            ),
        ],
    )


### Scons tool hooks ###


def generate(env):
    env.AddMethod(virtual_target_command, "VirtualTargetCommand")


def exists(env):
    return True

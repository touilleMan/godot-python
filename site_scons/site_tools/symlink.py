import os
from SCons.Script import Builder, COMMAND_LINE_TARGETS
from SCons.Util import is_List
from SCons.Errors import UserError


def SymlinkAction(target, source, env):
    target = target if is_List(target) else [target]
    source = source if is_List(source) else [source]

    if len(target) != 1 or len(source) != 1:
        raise UserError("Symlink only takes a single target and source")

    abs_src = os.path.abspath(str(source[0]))
    abs_trg = os.path.abspath(str(target[0]))

    if not os.path.isdir(abs_src):
        raise UserError("Only folder symlink are allowed due to Windows limitation")

    try:
        os.unlink(abs_trg)
    except Exception:
        pass

    if env["HOST_OS"] == "win32":
        try:
            import _winapi

            _winapi.CreateJunction(abs_src, abs_trg)
        except Exception as e:
            raise UserError(
                f"Can't do a NTFS junction as symlink fallback ({abs_src} -> {abs_trg})"
            ) from e

    else:
        try:
            os.symlink(abs_src, abs_trg)
        except Exception as e:
            raise UserError(f"Can't create symlink ({abs_src} -> {abs_trg})") from e


def SymlinkBuilder(env, target, source, action=SymlinkAction):
    results = env.Command(target, source, action)
    if env["HOST_OS"] == "win32":
        abs_trg = os.path.abspath(str(target[0]))

        def _rm(env, target, source):
            # assert len(target) == 1
            try:
                os.unlink(abs_trg)
            except FileNotFoundError:
                pass
            except Exception as e:
                raise UserError(f"Can't remove NTFS junction {abs_trg}") from e

        env.CustomClean(
            target,
            # RemoveSymlink
            env.Action(_rm, f"Removing symlink {abs_trg}"),
        )
    return results


def CustomClean(env, targets, action):
    # Inspired by https://github.com/SCons/scons/wiki/CustomCleanActions

    if not env.GetOption("clean"):
        return

    # normalize targets to absolute paths
    targets = [env.Entry(target).abspath for target in env.Flatten(targets)]
    launchdir = env.GetLaunchDir()
    topdir = env.Dir("#").abspath
    cl_targets = COMMAND_LINE_TARGETS

    if not cl_targets:
        cl_targets.append(".")

    for cl_target in cl_targets:
        if cl_target.startswith("#"):
            full_target = os.path.join(topdir, cl_target[:1])
        else:
            full_target = os.path.join(launchdir, cl_target)
        full_target = os.path.normpath(full_target)
        for target in targets:
            if target.startswith(full_target):
                env.Execute(action)
                return


### Scons tool hooks ###


def generate(env):
    """
    Scons doesn't provide cross-platform symlink out of the box due to Windows...
    """
    env.AddMethod(CustomClean, "CustomClean")
    env.Append(BUILDERS={"Symlink": SymlinkBuilder})


def exists(env):
    return True

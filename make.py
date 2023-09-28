#! /usr/bin/env python

from __future__ import annotations

import argparse
import itertools
import os
import random
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Iterable, Union


BASE_DIR = Path(__file__).parent.resolve()
# Use relative path by default for cleaner help output (BASE_DIR is used as cwd anyway)
BUILD_DIR = os.environ.get("BUILD_DIR", "build")


CYAN = "\x1b[36m"
GREY = "\x1b[37m"
PINK = "\x1b[35m"
BOLD_YELLOW = "\x1b[1;33m"
NO_COLOR = "\x1b[0;0m"
CUTENESS = [
    "ฅ^◕ﻌ◕^ฅ",
    "(^･㉨･^)∫",
    "^•ﻌ•^ฅ",
    "✺◟(⏓ᴥ⏓▽)◞✺",
    "ฅ(・㉨・˶)ฅ",
    "(ﾐꆤ ﻌ ꆤﾐ)∫",
    "(ﾐㆁ㉨ㆁﾐ)",
    "ฅ(=ච ω ච=)",
]


class Op:
    def display(self, extra_cmd_args: Iterable[str]) -> str:
        raise NotImplementedError

    def run(self, cwd: Path, extra_cmd_args: Iterable[str]) -> None:
        raise NotImplementedError


class Cwd(Op):
    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd

    def display(self, extra_cmd_args: Iterable[str]) -> str:
        return f"cd {GREY}{self.cwd.relative_to(BASE_DIR).as_posix()}{NO_COLOR}"


class Rmdir(Op):
    def __init__(self, target: Path) -> None:
        self.target = target

    def display(self, extra_cmd_args: Iterable[str]) -> str:
        return f"{CYAN}rm -rf {self.target.relative_to(BASE_DIR).as_posix()}{NO_COLOR}"

    def run(self, cwd: Path, extra_cmd_args: Iterable[str]) -> None:
        target = self.target if self.target.is_absolute() else cwd / self.target
        shutil.rmtree(target, ignore_errors=True)


class Echo(Op):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def display(self, extra_cmd_args: Iterable[str]) -> str:
        return f"{CYAN}echo {self.msg!r}{NO_COLOR}"

    def run(self, cwd: Path, extra_cmd_args: Iterable[str]) -> None:
        print(self.msg, flush=True)


class Cmd(Op):
    def __init__(
        self,
        cmd: str,
        extra_env: dict[str, str] = {},
    ) -> None:
        self.cmd = cmd
        self.extra_env = extra_env

    def cmd_with_extra_cmd_args(self, extra_cmd_args: Iterable[str]) -> str:
        cooked_extra_cmds_args = " ".join(extra_cmd_args) if extra_cmd_args else ""
        if "{extra_cmd_args}" in self.cmd:
            return self.cmd.format(extra_cmd_args=cooked_extra_cmds_args)
        else:
            return f"{self.cmd} {cooked_extra_cmds_args}"

    def display(self, extra_cmd_args: Iterable[str]) -> str:
        display_extra_env = " ".join(
            [f"{GREY}{k}={v}{NO_COLOR}" for k, v in self.extra_env.items()]
        )
        cmd = self.cmd_with_extra_cmd_args(extra_cmd_args)
        return f"{display_extra_env} {CYAN}{cmd}{NO_COLOR}"

    def run(self, cwd: Path, extra_cmd_args: Iterable[str]) -> None:
        args = self.cmd_with_extra_cmd_args(extra_cmd_args).split()
        subprocess.check_call(
            args,
            env={**os.environ, **self.extra_env},
            cwd=cwd,
        )


COMMANDS: dict[tuple[str, ...], Union[Op, tuple[Op, ...]]] = {
    ("init", "i"): (
        Cmd(f"meson setup {BUILD_DIR}"),
        Cmd(f"meson compile -C {BUILD_DIR}"),
    ),
    ("rebuild", "r"): (Cmd(f"meson compile -C {BUILD_DIR}"),),
    ("tests", "t"): (
        Cmd(f"python tests/run.py --build-dir={BUILD_DIR} {{extra_cmd_args}} -- --headless"),
    ),
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
            Tired of remembering multiple silly commands ? Now here is a single silly command to remember !

            Examples:
            python make.py init  # Initial setup & build
            python make.py rebuild  # Subsequent build
            python make.py tests -- --headless  # Additional args passed to subcommand
        """
        ),
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="🎵 The sound of silence 🎵")
    parser.add_argument("--dry", action="store_true", help="Don't actually run, just display")
    parser.add_argument(
        "command",
        help="The command to run",
        nargs="?",
        choices=list(itertools.chain.from_iterable(COMMANDS.keys())),
        metavar="command",
    )

    # Handle `-- <extra_cmd_args>` in argv
    # (argparse doesn't understand `--`, so we have to implement it by hand)
    has_reached_cmd_extra_args = False
    extra_cmd_args = []
    argv = []
    for arg in sys.argv[1:]:
        if has_reached_cmd_extra_args:
            extra_cmd_args.append(arg)
        elif arg == "--":
            has_reached_cmd_extra_args = True
        else:
            argv.append(arg)

    args = parser.parse_args(argv)
    if not args.command:
        print("Available commands:\n")
        for aliases, cmds in COMMANDS.items():
            print(f"{BOLD_YELLOW}{', '.join(aliases)}{NO_COLOR}")
            cmds = (cmds,) if isinstance(cmds, Op) else cmds
            display_cmds = [cmd.display(extra_cmd_args) for cmd in cmds]
            join = f"{GREY}; and {NO_COLOR}" if "fish" in os.environ.get("SHELL", "") else " && "
            print(f"\t{join.join(display_cmds)}\n")

    else:
        for aliases, cmds in COMMANDS.items():
            if args.command in aliases:
                cmds = (cmds,) if isinstance(cmds, Op) else cmds
                break
        else:
            raise SystemExit(f"Unknown command alias `{args.command}`")

        cwd = BASE_DIR
        for cmd in cmds:
            if not args.quiet:
                # Flush is required to prevent mixing with the output of sub-command
                print(f"{cmd.display(extra_cmd_args)}\n", flush=True)
                if not isinstance(cmd, Cwd):
                    try:
                        print(f"{PINK}{random.choice(CUTENESS)}{NO_COLOR}", flush=True)
                    except UnicodeEncodeError:
                        # Windows crappy term couldn't encode kitty unicode :'(
                        pass

            if args.dry:
                continue

            if isinstance(cmd, Cwd):
                cwd = cmd.cwd
            else:
                try:
                    cmd.run(cwd, extra_cmd_args)
                except subprocess.CalledProcessError as err:
                    raise SystemExit(str(err)) from err

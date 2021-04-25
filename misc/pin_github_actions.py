#! /usr/bin/env python
#
# see: https://julienrenaux.fr/2019/12/20/github-actions-security-risk/
# TL;DR: Using GitHub actions with branch names or tags is unsafe. Use commit hash instead.


import re
import sys
import json
import argparse
from pathlib import Path
from functools import lru_cache
from urllib.request import urlopen


GITHUB_CONF_DIR = Path(".").joinpath("../.github").resolve()
REPO_REGEX = r"(?P<repo>[\w\-_]+/[\w\-_]+)"
SHA_REGEX = r"(?P<sha>[a-fA-F0-9]{40})"
TAG_REGEX = r"(?P<tag>[\w\-_]+)"
PIN_REGEX = r"(?P<pin>[\w\-_]+)"
USES_REGEX = re.compile(
    rf"uses\W*:\W*{REPO_REGEX}@({SHA_REGEX}|{TAG_REGEX})(\W*#\W*pin@{PIN_REGEX})?", re.MULTILINE
)


def get_files(pathes):
    for path in pathes:
        if path.is_dir():
            yield from path.rglob("*.yml")
        elif path.is_file():
            yield path


@lru_cache(maxsize=None)
def resolve_tag(repo, tag):
    url = f"https://api.github.com/repos/{repo}/git/ref/tags/{tag}"
    with urlopen(url) as f:
        data = json.loads(f.read())
        return data["object"]["sha"]


def add_pin(pathes):
    for file in get_files(pathes):
        txt = file.read_text()
        overwrite_needed = False
        # Start by the end so that we can use match.start/end to do in-place modifications
        for match in reversed(list(USES_REGEX.finditer(txt))):
            repo = match.group("repo")
            tag = match.group("tag")
            if tag is not None:
                sha = resolve_tag(repo, tag)
                print(f"Pinning github action {file}: {repo}@{tag} => {sha}")
                txt = txt[: match.start()] + f"uses: {repo}@{sha}  # pin@{tag}" + txt[match.end() :]
                overwrite_needed = True
        if overwrite_needed:
            file.write_text(txt)
    return 0


def check_pin(pathes):
    ret = 0
    for file in get_files(pathes):
        for match in USES_REGEX.finditer(file.read_text()):
            repo = match.group("repo")
            tag = match.group("tag")
            if tag is not None:
                print(f"Unpinned github action {file}: {repo}@{tag}")
                ret = 1
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["check", "add"])
    parser.add_argument(
        "files", nargs="*", type=Path, default=[Path(__name__).joinpath("../.github/").resolve()]
    )

    args = parser.parse_args()
    if args.cmd == "check":
        sys.exit(check_pin(args.files))
    else:
        sys.exit(add_pin(args.files))

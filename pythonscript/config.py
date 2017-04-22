from __future__ import print_function
import sys
from os import path
import subprocess


PY_DIR = path.dirname(path.abspath(__file__)) + '/cpython'
PY_TARGET = PY_DIR + "/libpython3.6m.a"
PY_DEBUG_TARGET = PY_DIR + "/libpython3.6dm.a"


def can_build(platform):
    return True


def run_and_shutup(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()
    print(' '.join(cmd))
    proc = subprocess.Popen(cmd, cwd=PY_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        print(err, file=sys.stderr)
        raise RuntimeError('Command %s failed' % cmd)


def configure(env):
    # TODO: use ptrcall for the binding
    # env.use_ptrcall = True
    target = PY_TARGET if env["target"] != "debug" else PY_DEBUG_TARGET
    if not path.isfile(target):
        print('Building libpython (output skipped)...')
        if not path.isfile('Makefile'):
            cmd = ['./configure', '--enable-shared', '--prefix=%s/build' % PY_DIR]
            if env["target"] == "debug":
                cmd.append('--with-pydebug')
            run_and_shutup(cmd)
        run_and_shutup('make')
        run_and_shutup('make install')
        print('libpython successfully built !')

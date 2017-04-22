from __future__ import print_function
import sys
from os import path, environ
import subprocess


PY_DIR = path.dirname(path.abspath(__file__)) + '/cpython'
PY_TARGET = PY_DIR + "/libpython3.6m.a"
PY_DEBUG_TARGET = PY_DIR + "/libpython3.6dm.a"


def can_build(platform):
    return True


def run_and_shutup(cmd, cwd=PY_DIR, **kwargs):
    if isinstance(cmd, str):
        cmd_str = cmd
        cmd = cmd.split()
    else:
        cmd_str = ' '.join(cmd)
    print(cmd_str)
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    out, err = proc.communicate()
    if proc.returncode:
        print(err, file=sys.stderr)
        raise RuntimeError('Command %s failed' % cmd_str)


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
        run_and_shutup('make -j4')
        run_and_shutup('make install')
        # Install cffi is a pita...
        cmd_env = environ.copy()
        cmd_env['LD_LIBRARY_PATH'] = PY_DIR
        run_and_shutup('%s/build/bin/pip3 install cffi' % PY_DIR, env=cmd_env)
        print('libpython successfully built !')

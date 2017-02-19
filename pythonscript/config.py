from os import path
import subprocess


PY_DIR = path.dirname(path.abspath(__file__)) + '/cpython'
PY_TARGET = PY_DIR + "/libpython3.6m.a"
PY_DEBUG_TARGET = PY_DIR + "/libpython3.6dm.a"


def can_build(platform):
    return True


def configure(env):
    env.use_ptrcall = True
    if ((env["target"] == "debug" and not path.isfile(PY_DEBUG_TARGET)) or
            not path.isfile(PY_TARGET)):
        print('Building libpython...')
        if not path.isfile('Makefile'):
            cmd = ['./configure', '--enable-shared --prefix=%s/build' % PY_DIR]
            if env["target"] == "debug":
                cmd.append('--with-pydebug')
            subprocess.call(cmd, cwd=PY_DIR)
        subprocess.call(['make'], cwd=PY_DIR)
        print('libpython successfully built !')

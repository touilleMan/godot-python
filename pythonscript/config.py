from os import path
import subprocess


PY_DIR = path.dirname(path.abspath(__file__)) + '/cpython'
PY_TARGET = PY_DIR + "/libpython3.6m.a"
PY_DEBUG_TARGET = PY_DIR + "/libpython3.6dm.a"


def can_build(platform):
    return True


def configure(env):
    # TODO: use ptrcall for the binding
    # env.use_ptrcall = True
    target = PY_TARGET if env["target"] != "debug" else PY_DEBUG_TARGET
    if not path.isfile(target):
        print('Building libpython...')
        if not path.isfile('Makefile'):
            cmd = ['./configure', '--enable-shared', '--prefix=%s/build' % PY_DIR]
            if env["target"] == "debug":
                cmd.append('--with-pydebug')
            subprocess.call(cmd, cwd=PY_DIR)
        subprocess.call(['make'], cwd=PY_DIR)
        subprocess.call(['make', 'install'], cwd=PY_DIR)
        print('libpython successfully built !')

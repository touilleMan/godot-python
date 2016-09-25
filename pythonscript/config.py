from os import path
import subprocess


MP_DIR = path.dirname(path.abspath(__file__)) + '/micropython'
MP_TARGET = MP_DIR + "/libmicropython.a"


def can_build(platform):
  return True


def configure(env):
    if not path.isfile(MP_TARGET):
        print('Building libmicropython.a...')
        subprocess.call(["make"], cwd=MP_DIR)
        print('libmicropython.a successfully built !')

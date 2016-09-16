from os import path
import subprocess


TOP = path.dirname(path.abspath(__file__))
MPTOP = TOP + "/micropython"


def can_build(platform):
  return True


def configure(env):
	subprocess.call("make -f {MPTOP}/examples/embedding/Makefile.upylib MPTOP={MPTOP}".format(MPTOP=MPTOP).split(), cwd=TOP)

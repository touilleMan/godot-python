from SCons.Util import is_List
from SCons.Action import Action
from urllib.request import urlopen


def Download(env, target, url):
    def _do_download(target, source, env):
        if not target:
            target = []
        elif not is_List(target):
            target = [target]
        with urlopen(url) as infd:
            with open(target[0].abspath, "bw") as outfd:
                outfd.write(infd.read())

    return env.Command(target, None, Action(_do_download, f"Download {url}"))


### Scons tool hooks ###


def generate(env):
    env.AddMethod(Download, "Download")


def exists(env):
    return True

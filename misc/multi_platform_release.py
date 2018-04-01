#! /bin/usr/env python3

"""
Build system is designed to created a build targetting a single platform.
This script aims at bundle together multiple builds to generate a final
multip-platform release.
"""

import argparse
import os
import shutil
from urllib.request import urlretrieve
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor


BASEDIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = 'https://github.com/touilleMan/godot-python/releases/download'
DEFAULT_PLATFORMS = [
    'osx-64-cpython',
    # 'osx-64-pypy',
    'windows-32-cpython',
    # 'windows-32-pypy',
    'windows-64-cpython',
    'x11-64-cpython',
    # 'x11-64-pypy',
]


def fetch_build(src, version, platform):
    build_zipname = 'godot-python-%s-%s.zip' % (version, platform)
    if src.startswith('http://') or src.startswith('https://'):
        cache_file = build_zipname
        if not os.path.exists(cache_file):
            url = '%s/%s/%s' % (src, version, build_zipname)
            urlretrieve(url, filename=build_zipname, reporthook=lambda *args: print('.', end='', flush=True))
        return ZipFile(cache_file)
    else:
        return ZipFile('%s/%s' % (src, build_zipname))


def extract_build(platform, zipobj, dst):
    build_dst = '%s/pythonscript/%s' % (dst, platform)
    extract_tmp = '%s-tmp' % build_dst
    zipobj.extractall(extract_tmp)
    shutil.move('%s/pythonscript' % extract_tmp, build_dst)
    shutil.rmtree(extract_tmp)
    return zipobj


def extract_bonuses(zipobj, dst):
    zipobj.extract('README.txt', dst)
    zipobj.extract('LICENSE.txt', dst)
    return zipobj


def pipeline_executor(platform, version, src, dst):

    print('%s - fetch build...' % platform)
    zipbuild = fetch_build(src, version, platform)

    print('%s - extract build...' % platform)
    extract_build(platform, zipbuild, dst)


def orchestrator(platforms, version, src, dst, buildzip):
    futures = []
    with ThreadPoolExecutor() as executor:
        for platform in platforms:
            futures.append(executor.submit(
                pipeline_executor, platform, version, src, dst))
    for future in futures:
        if not future.cancelled():
            future.result()  # Raise exception if any

    if extract_bonuses:
        print('add bonuses...')
        shutil.copy(
            '%s/../extras/pythonscript.gdnlib' % BASEDIR,
            '%s/pythonscript.gdnlib' % dst
        )
        shutil.copy(
            '%s/../extras/release_LICENSE.txt' % BASEDIR,
            '%s/LICENSE.txt' % dst
        )
        shutil.copy(
            '%s/../extras/release_README.txt' % BASEDIR,
            '%s/README.txt' % dst
        )

    if buildzip:
        print('zipping result...')
        shutil.make_archive(dst, 'zip', dst)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--platforms', nargs='+', default=DEFAULT_PLATFORMS)
    parser.add_argument('--src', default=DEFAULT_SRC)
    parser.add_argument('--version', required=True)
    parser.add_argument('--zip', action='store_false')
    args = parser.parse_args()

    dst = 'pythonscript-%s' % args.version
    try:
        shutil.os.mkdir(dst)
        shutil.os.mkdir('%s/pythonscript' % dst)
    except:
        pass

    orchestrator(args.platforms, args.version, args.src, dst, args.zip)


if __name__ == '__main__':
    main()

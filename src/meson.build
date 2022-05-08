##############################################################################
#                                  Config                                    #
##############################################################################


# Must handle .pxd by hand given
pxd_deps = []
pxd_depfiles = []


# Retreive all the .py files, this is needed for two things:
# 1 - To install them
# 2 - To copy them in the build dir. This is required due to how Cython
#     import/cimport works.


py_srcs = [
    'godot/__init__.py',
    'godot/_version.py',
    'godot/_hazmat/__init__.py'
]
py_in_buildir_dsts = []


foreach src: py_srcs
    item_dir = fs.parent(src)
    install_data(
        src,
        install_dir: join_paths(python_site_packages_install_path, item_dir)
    )
    py_in_buildir_dsts += join_paths(meson.current_build_dir(), src)
endforeach


copy_py_in_buildir = custom_target(
    output: 'py_copied_marker',  # Cannot specify real outputs given they are the same as inputs
    input: py_srcs,
    command: [
        python,
        '-c',
        '''
import sys, shutil
src_and_dst = sys.argv[1:-1]
assert len(src_and_dst) % 2 == 0
count = len(src_and_dst) // 2
for src, dst in zip(src_and_dst[:count], src_and_dst[count:]):
    shutil.copyfile(src, dst)
open(sys.argv[-1], "w").write("")  # finish with dummy file
''',
        '@INPUT@',
        py_in_buildir_dsts,
        '@OUTPUT@'
    ]
)


##############################################################################
#                       Load subdirs (and it config)                         #
##############################################################################


subdir('godot')


##############################################################################
#                                Compilation                                 #
##############################################################################


# _pythonscript.so
# └─ _pythonscript.c
#     └─ _pythonscript.pyx
#         └─ gdnative_interface.pxd
#             └─ gdnative_interface.h
# libpythonscript.so
# ├─ pythonscript.c
# └─ _pythonscript_api.h
#
# Note we cannot bundle `_pythonscript.so` within `libpythonscript.so` due
# to how Python loads native modules.


# `_pythonscript_api.h` is used to expose the Python callback used by `pythonscript.c`,
# hence this header is private and won't be provided in the release
pyx_pythonscript_c = custom_target('_pythonscript',
    output : ['_pythonscript.c', '_pythonscript_api.h'],
    input : '_pythonscript.pyx',
    depends: [gdnative_interface_pxd],
    command : [cython, '-3', '--fast-fail', '@INPUT@', '-o', '@OUTPUT0@']
)


pyx_pythonscript_lib = shared_library(
    '_pythonscript',
    pyx_pythonscript_c,
    dependencies : [libgodot, libpython],
    install_rpath: '$ORIGIN/lib',
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: python_site_packages_install_path,
)


pyx_pythonscript = declare_dependency(
    include_directories: pyx_pythonscript_lib.private_dir_include(),  # To expose _pythonscript_api.h
    link_with: pyx_pythonscript_lib,
)


shared_library(
    'pythonscript',
    'pythonscript.c',
    dependencies: [libgodot, libpython, pyx_pythonscript],
    install_rpath: '$ORIGIN/lib',
    install: true,
    install_dir: 'addons/pythonscript/' + host_platform,
)

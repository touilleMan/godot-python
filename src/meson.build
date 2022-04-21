subdir('godot')

cc = meson.get_compiler('c')

# libpythonscript.so
# ├─ libpyx_pythonscript.a
# |   └─ _pythonscript.c
# |       └─ _pythonscript.pyx
# └─ pythonscript.c

# `_pythonscript_api.h` is used to expose the Python callback used by `pythonscript.c`,
# hence this header is private and won't be provided in the release
pyx_pythonscript_c = custom_target('_pythonscript',
    output : ['_pythonscript.c', '_pythonscript_api.h'],
    input : '_pythonscript.pyx',
    command : [cython, '-3', '--fast-fail', '@INPUT@', '-o', '@OUTPUT0@']
)

pyx_pythonscript_lib = static_library(
    'pyx_pythonscript',
    pyx_pythonscript_c,
    dependencies : [libgodot, libpython],
)

pyx_pythonscript = declare_dependency(
    link_with: pyx_pythonscript_lib,
    include_directories: pyx_pythonscript_lib.private_dir_include(),  # To expose _pythonscript_api.h
    sources: [pyx_pythonscript_c],
)

shared_library(
    'pythonscript',
    'pythonscript.c',
    dependencies: [libgodot, libpython, pyx_pythonscript],
    install_rpath: '$ORIGIN/lib',
    install: true,
    install_dir: 'addons/pythonscript/' + host_platform,
)

subdir('godot')

cc = meson.get_compiler('c')

pyx_pythonscript_c = custom_target('_pythonscript',
    output : ['_pythonscript.c', '_pythonscript_api.h'],
    input : '_pythonscript.pyx',
    depend_files: [],
    command : [cython, '-3', '--fast-fail', '@INPUT@', '-o', '@OUTPUT0@']
)
pyx_pythonscript_lib = static_library(
    'pyx_pythonscript',
    pyx_pythonscript_c,
    # On Windows `/MDd` flag (used by meson when `buildtype=debug`) define `_DEBUG`,
    # however this make `python.h` (`pyconfig.h` actually) to consider we should link
    # against `python39_d.lib`, but we only have `python39.lib` available...
    c_args: '-U_DEBUG',
    dependencies : libpython,
)
pyx_pythonscript = declare_dependency(
    link_with: pyx_pythonscript_lib,
    include_directories: pyx_pythonscript_lib.private_dir_include(),  # To expose _pythonscript_api.h
)

shared_library(
    'pythonscript',
    'pythonscript.c',
    include_directories: [
        '../custom_godot_headers/'
    ],
    c_args: ['-DGODOT_VERSION_MAJOR=4', '-DGODOT_VERSION_MINOR=0', '-U_DEBUG'],
    dependencies: [libpython, pyx_pythonscript],
)

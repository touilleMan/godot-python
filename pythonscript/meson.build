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
    dependencies : libpython,
)
pyx_pythonscript = declare_dependency(
    link_with: pyx_pythonscript_lib,
    include_directories: pyx_pythonscript_lib.private_dir_include(),  # To expose _pythonscript_api.h
    sources: [pyx_pythonscript_lib, pyx_pythonscript_c],
)


shared_library(
    'pythonscript',
    'pythonscript.c',
    include_directories: [
        '../custom_godot_headers/'
    ],
    c_args: ['-DGODOT_VERSION_MAJOR=4', '-DGODOT_VERSION_MINOR=0', ],
    dependencies: [libpython, pyx_pythonscript],
)

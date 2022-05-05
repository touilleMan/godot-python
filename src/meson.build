subdir('godot')

# libpythonscript.so
# └─ pythonscript.c
# _pythonscript.so
# └─ _pythonscript.c
#     └─ _pythonscript.pyx
#
# Note we cannot bundle `_pythonscript.so` within `libpythonscript.so` due
# to how Python loads native modules.

# `_pythonscript_api.h` is used to expose the Python callback used by `pythonscript.c`,
# hence this header is private and won't be provided in the release
pyx_pythonscript_c = custom_target('_pythonscript',
    output : ['_pythonscript.c', '_pythonscript_api.h'],
    input : '_pythonscript.pyx',
    command : [cython, '-3', '--fast-fail', '@INPUT@', '-o', '@OUTPUT0@']
)

# Python native module must have custom naming:
# `foo.pyd` on Windows, `foo.so` on linux/macos
if host_platform.startswith('windows')
    python_native_module_name_prefix = ''
    python_native_module_name_suffix = 'pyd'
else
    python_native_module_name_prefix = ''
    python_native_module_name_suffix = 'so'
endif

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
)

shared_library(
    'pythonscript',
    'pythonscript.c',
    dependencies: [libgodot, libpython, pyx_pythonscript],
    install_rpath: '$ORIGIN/lib',
    install: true,
    install_dir: 'addons/pythonscript/' + host_platform,
)

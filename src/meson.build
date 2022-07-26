##############################################################################
#                              .pxd generation                               #
##############################################################################


# .pxd files are used for .pyx compilation, hence the generated .pxd must be
# created early on.
# However we cannot just put the generation code in the directory the .pxd should
# resides given this folder may also contain a .pyx that requires `_pythonscript.so`
# which itself requires the generated .pxd !
# The "good" solution to this would be to be able to specify subfolder in output
# parameter, but this is not allowed by meson...
# So what we do here is:
# - generate the .pxd files here with it actual path encoded in it name (i.e.
#   `foo/bar/spam.pxd` becomes `foo#bar#spam.pxd`)
# - we use those .pxd to build `_pythonscript.so`
# - we then enter sub directories and do the remaining .pyx compilation.
# - in the sub directories, we also have custom rules to copy the generated
#   .pxd files in their expected location (only needed for the install step)
# see https://github.com/mesonbuild/meson/issues/2320#issuecomment-1147929155


# godot/_hazmat/gdnative_interface.pxd
# └─ gdnative_interface.h


# Convert the header file frome C to Cython
pxd_godot_hazmat_gdnative_interface = custom_target(
    output: 'godot#_hazmat#gdnative_interface.pxd',
    input: [
        join_paths(scripts_dir, 'generate_gdnative_interface_pxd.py'),
        join_paths(godot_headers_path, 'godot/gdnative_interface.h')
    ],
    command: [python, '@INPUT0@', '--input', '@INPUT1@', '--output', '@OUTPUT@'],
)


# godot/builtins.pxd
# └─ extension_api.json


if host_machine.cpu_family() == 'x86_64'
    builtins_build_config = 'double_64'
elif host_machine.cpu_family() == 'x86'
    builtins_build_config = 'double_32'
else
    error('Unsupported CPU familly' + host_machine.cpu_family())
endif


generate_builtins_input = [
    join_paths(scripts_dir, 'generate_builtins.py'),  # Must stay first !
    godot_extension_api_json,  # Must stay second !
    files(
        'godot/_builtins.tmpl.pyx',
        'godot/_builtins.tmpl.pxd',
        'godot/_builtins.tmpl.pyi',
        'godot/_builtin.tmpl.pxi',
    ),
]


generate_builtins_command = [
    python,
    '@INPUT0@',  # generate_builtins.py
    '--input',
    '@INPUT1@',  # extension_api.json
    '--build-config',
    builtins_build_config,
    '--output',
    '@OUTPUT0@',
]


pxd_godot__builtins = custom_target(
    output: 'godot#_builtins.pxd',
    input: generate_builtins_input,
    command: generate_builtins_command,
)


##############################################################################
#          _pythonscript.pyx compilation (required by other .pyx)            #
##############################################################################


# _pythonscript.so
# └─ _pythonscript.c
#     └─ _pythonscript.pyx
#         └─ gdnative_interface.pxd
#             └─ ...


# `_pythonscript_api.h` is used to expose the Python callbacks used by `pythonscript.c`,
# `_pythonscript.h` is used to expose the Godot APIs pointer to other Cython modules,
# hence those headers are private and won't be provided in the release
c_pythonscript = custom_target('_pythonscript.c & _pythonscript.h & _pythonscript_api.h}',
    output : ['_pythonscript.c', '_pythonscript.h', '_pythonscript_api.h'],
    input : ['_pythonscript.pyx', pxd_godot__builtins, pxd_godot_hazmat_gdnative_interface],
    command : cythonize_command,
)
h_pythonscript_api = c_pythonscript[2]  # Header for pythonscript.c
h_pythonscript = c_pythonscript[1]  # Header for other Cython modules
c_pythonscript = c_pythonscript[0]


if host_platform.startswith('linux')
    lib__pythonscript_rpath = '$ORIGIN/../..'
elif host_platform.startswith('macos')
    lib__pythonscript_rpath = '@loader_path/../..'
else
    lib__pythonscript_rpath = ''
endif


lib__pythonscript = shared_library(
    '_pythonscript',
    c_pythonscript,
    dependencies : [dep_godot, dep_python],
    install_rpath: lib__pythonscript_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: python_site_packages_install_path,
)


dep__pythonscript = declare_dependency(
    # include_directories: lib__pythonscript.private_dir_include(),  # To expose _pythonscript_api.h
    sources: [h_pythonscript, h_pythonscript_api],
    link_with: lib__pythonscript,
)


##############################################################################
#                     Load subdirs (and their config)                        #
##############################################################################


subdir('godot')


##############################################################################
#                                 Compilation                                #
##############################################################################


# libpythonscript.so
# ├─ pythonscript.c
# └─ _pythonscript_api.h
#    └─ ...


# Note we cannot bundle `_pythonscript.so` within `libpythonscript.so` due
# to how Python loads native modules.


if host_platform.startswith('linux')
    lib_pythonscript_rpath = '$ORIGIN/lib'
elif host_platform.startswith('macos')
    lib_pythonscript_rpath = '@loader_path/lib'
else
    lib_pythonscript_rpath = ''
endif


lib_pythonscript = shared_library(
    'pythonscript',
    ['pythonscript.c'],
    dependencies: [dep_godot, dep_python, dep__pythonscript],
    install_rpath: lib_pythonscript_rpath,  # To find libpython
    install: true,
    install_dir: 'addons/pythonscript/' + host_platform,
)

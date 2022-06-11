##############################################################################
#                     Load subdirs (and their config)                        #
##############################################################################


subdir('_hazmat')


##############################################################################
#                                  Config                                    #
##############################################################################


pxds_godot = [
    pxds_godot_hazmat,
    pxd_godot__builtins,  # Generated in `src/meson.build`
]


##############################################################################
#                           Small fries to install                           #
##############################################################################


foreach src: ['__init__.py', '_version.py']
    install_data(
        src,
        install_dir: join_paths(python_site_packages_install_path, 'godot'),
    )
endforeach


custom_target(
    output: '_builtins.pxd',
    input: pxd_godot__builtins,
    command: copy_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


custom_target(
    output: '_builtins.pyi',
    input: generate_builtins_input,
    command: generate_builtins_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


##############################################################################
#                                Compilation                                 #
##############################################################################


# _builtins.so
# └─ _builtins.c
#     ├─ gdnative_interface.pxd
#     │  └─ ...
#     └─ _builtins.pyx
#         └─ extension_api.json


pyx_builtins = custom_target(
    output: '_builtins.pyx',
    input: generate_builtins_input,
    command: generate_builtins_command,
)


c_builtins = custom_target(
    output : '_builtins.c',
    input : [pyx_builtins, pxds_godot],
    command : cythonize_command,
)


shared_library(
    '_builtins',
    c_builtins,
    dependencies : [dep_godot, dep_python, dep_pythonscript],
    install_rpath: '$ORIGIN/../../..',  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)

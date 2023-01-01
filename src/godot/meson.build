##############################################################################
#                     Load subdirs (and their config)                        #
##############################################################################


subdir('hazmat')


##############################################################################
#                           Small fries to install                           #
##############################################################################


foreach src: ['__init__.py', '__init__.pyi', 'py.typed']
    install_data(
        src,
        install_dir: join_paths(python_site_packages_install_path, 'godot'),
    )
endforeach


configure_file(
    input : '_version.in.py',
    output : '_version.py',
    configuration : {'version': meson.project_version()},
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


custom_target(
    output: 'builtins.pxd',
    input: pxd_godot_builtins,
    command: copy_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


custom_target(
    output: 'builtins.pyi',
    input: [
        generate_tmpl_base_input,
        files('builtins.pyi.j2'),
    ],
    command: generate_tmpl_cmd,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


custom_target(
    output: 'classes.pxd',
    input: pxd_godot_classes,
    command: copy_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


custom_target(
    output: 'classes.pyi',
    input: [
        generate_tmpl_base_input,
        files('classes.pyi.j2'),
    ],
    command: generate_tmpl_cmd,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


##############################################################################
#                                Compilation                                 #
##############################################################################


# builtins.so
# └─ builtins.c
#    ├─ gdextension_interface.pxd
#    │  └─ ...
#    └─ builtins.pyx
#       └─ extension_api.json

pyxbuiltins = custom_target(
    output: 'builtins.pyx',
    input: [
        generate_tmpl_base_input,
        files(
            'builtins.pyx.j2',
            'builtins_pyx/class.pyx.j2',
            'builtins_pyx/constructor.pyx.j2',
            'builtins_pyx/conversion.pyx.j2',
            'builtins_pyx/member.pyx.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


cbuiltins = custom_target(
    output : 'builtins.c',
    input : [pyxbuiltins, pxds_godot],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    builtins_rpath = '$ORIGIN/../../..'
elif host_platform.startswith('macos')
    builtins_rpath = '@loader_path/../../..'
else
    builtins_rpath = ''
endif


# AutoPxd currently strip const qualifier when generating `gdextension_interface.pxd`,
# hence -Wno-discarded-qualifiers
if host_platform.startswith('windows')
    builtins_c_args = []
else
    builtins_c_args = ['-Wno-discarded-qualifiers', '-Wno-incompatible-pointer-types-discards-qualifiers']
endif


shared_library(
    'builtins',
    cbuiltins,
    c_args: builtins_c_args,
    dependencies : [dep_godot, dep_python, dep_pythonscript],
    install_rpath: builtins_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


# classes.so
# └─ classes.c
#    ├─ gdextension_interface.pxd
#    │  └─ ...
#    └─ classes.pyx
#       └─ extension_api.json

pyxclasses = custom_target(
    output: 'classes.pyx',
    input: [
        generate_tmpl_base_input,
        files(
            'classes.pyx.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


cclasses = custom_target(
    output : 'classes.c',
    input : [pyxclasses, pxds_godot],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    classes_rpath = '$ORIGIN/../../..'
elif host_platform.startswith('macos')
    classes_rpath = '@loader_path/../../..'
else
    classes_rpath = ''
endif


# Cython's cdef inline methods are turned into static inline C functions that
# produced `defined but not used` errors, hence the `-Wno-unused-function`
# AutoPxd currently strip const qualifier when generating `gdextension_interface.pxd`,
# hence -Wno-discarded-qualifiers
if host_platform.startswith('windows')
    classes_c_args = []
else
    classes_c_args = ['-Wno-discarded-qualifiers', '-Wno-incompatible-pointer-types-discards-qualifiers', '-Wno-unused-function']
endif


shared_library(
    'classes',
    cclasses,
    c_args: classes_c_args,
    dependencies : [dep_godot, dep_python, dep_pythonscript],
    install_rpath: classes_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)

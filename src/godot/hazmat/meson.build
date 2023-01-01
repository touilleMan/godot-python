##############################################################################
#                           Small fries to install                           #
##############################################################################


foreach src: ['__init__.py', 'extension_class.pxd']
    install_data(
        src,
        install_dir: join_paths(python_site_packages_install_path, 'godot', 'hazmat'),
    )
endforeach


custom_target(
    output: 'gdextension_interface.pxd',
    input: pxd_godot_hazmat_gdextension,
    command: copy_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot', 'hazmat'),
)

custom_target(
    output: 'gdnative_ptrs.pxd',
    input: [pxd_godot_hazmat_gdnative_ptrs],
    command: copy_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot', 'hazmat'),
)


custom_target(
    output: 'gdapi.pxd',
    input: pxd_godot_hazmat_gdapi,
    command: copy_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot', 'hazmat'),
)



##############################################################################
#                                Compilation                                 #
##############################################################################


# gdnative_ptrs.so
# └─ gdnative_ptrs.c
#    ├─ gdextension_interface.pxd
#    │  └─ ...
#    └─ gdapi_ptrs.pyx
#       └─ extension_api.json


pyx_gdnative_ptrs = custom_target(
    output: 'gdnative_ptrs.pyx',
    input: [
        generate_tmpl_base_input,
        files(
            'gdnative_ptrs.pyx.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


c_gdnative_ptrs = custom_target(
    output : 'gdnative_ptrs.c',
    input : [
        pyx_gdnative_ptrs,
        pxd_godot_hazmat_gdapi,
        pxd_godot_hazmat_gdextension,
        pxd_godot_hazmat_gdnative_ptrs,
    ],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    gdnative_ptrs_rpath = '$ORIGIN/../../../..'
elif host_platform.startswith('macos')
    gdnative_ptrs_rpath = '@loader_path/../../../..'
else
    gdnative_ptrs_rpath = ''
endif


shared_library(
    'gdnative_ptrs',
    c_gdnative_ptrs,
    dependencies : [dep_godot, dep_python, dep_pythonscript],
    install_rpath: gdnative_ptrs_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot/hazmat'),
)



##############################################################################
#                                Compilation                                 #
##############################################################################


c_extension_class = custom_target(
    output : 'extension_class.c',
    input : [
        files('extension_class.pyx'),
        pxds_godot_hazmat,
    ],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    extension_class_rpath = '$ORIGIN/../../../..'
elif host_platform.startswith('macos')
    extension_class_rpath = '@loader_path/../../../..'
else
    extension_class_rpath = ''
endif


shared_library(
    'extension_class',
    c_extension_class,
    dependencies : [dep_godot, dep_python, dep_pythonscript],
    install_rpath: extension_class_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot/hazmat'),
)

##############################################################################
#                           Small fries to install                           #
##############################################################################


foreach src: ['__init__.py', 'gdapi.pxd']
    install_data(
        src,
        install_dir: join_paths(python_site_packages_install_path, 'godot', '_hazmat'),
    )
endforeach


custom_target(
    output: 'gdnative_interface.pxd',
    input: pxd_godot__hazmat_gdnative_interface,
    command: copy_command,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot', '_hazmat'),
)


##############################################################################
#                                Compilation                                 #
##############################################################################


# gdapi.so
# └─ gdapi.c
#    ├─ gdnative_interface.pxd
#    │  └─ ...
#    ├─ gdapi.pyx
#    └─ gdapi_ptrs.pxi
#       └─ extension_api.json


pxi_gdapi_ptrs = custom_target(
    output: 'gdapi_ptrs.pxi',
    input: [
        generate_tmpl_base_input,
        files(
            'gdapi_ptrs.tmpl.pxi',
        ),
        pxd_godot__hazmat_gdnative_interface,
    ],
    command: generate_tmpl_cmd,
)


c_gdapi = custom_target(
    output : 'gdapi.c',
    input : [
        files(
            'gdapi.pyx',
            'gdapi.pxd',
        ),
        pxi_gdapi_ptrs,
        pxds_godot__hazmat,
    ],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    gdapi_rpath = '$ORIGIN/../../../..'
elif host_platform.startswith('macos')
    gdapi_rpath = '@loader_path/../../../..'
else
    gdapi_rpath = ''
endif


shared_library(
    'gdapi',
    c_gdapi,
    dependencies : [dep_godot, dep_python, dep_pythonscript],
    install_rpath: gdapi_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot/_hazmat'),
)

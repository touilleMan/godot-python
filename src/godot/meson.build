##############################################################################
#                                  Config                                    #
##############################################################################



##############################################################################
#                       Load subdirs (and it config)                         #
##############################################################################


subdir('_hazmat')


##############################################################################
#                                Compilation                                 #
##############################################################################


# _bindings.so
# └─ _bindings.c
#     └─ _bindings.pyx
#         ├─ gdnative_interface.pxd
#         │   └─ gdnative_interface.h
#         └─ extension_api.json


generate_builtins_tmplts = [
    join_paths(scripts_dir, 'generate_builtins.py'),  # Must stay first !
    join_paths(scripts_dir, 'builtins_templates/builtins.tmpl.pyx'),
    join_paths(scripts_dir, 'builtins_templates/builtin.tmpl.pxi'),
]


if host_machine.cpu_family() == 'x86_64'
    builtins_build_config = 'double_64'
elif host_machine.cpu_family() == 'x86'
    builtins_build_config = 'double_32'
else
    error('Unsupported CPU familly' + host_machine.cpu_family())
endif


builtins_tgt = custom_target('generate bindings pyx,pxi,pxd',
    output: ['_bindings.pyx', '_bindings.pxd', '_bindings.pyi'],
    input: [godot_extension_api_json, generate_builtins_tmplts],
    command: [
        python,
        '@INPUT1@',
        '--input',
        '@INPUT0@',
        '--build-config',
        builtins_build_config,
        '--output',
        '@OUTPUT0@',
    ],
    install: true,
    # Only install .pxd and .pyi
    install_dir: [
        false,
        join_paths(python_site_packages_install_path, 'godot'),
        join_paths(python_site_packages_install_path, 'godot'),
    ]
)


builtins_c = custom_target('generate _builtins.c',
    output : '_builtins.c',
    input : builtins_tgt,
    command : [
        cython,
        '-3',
        '--fast-fail',
        '@INPUT0@',
        '-I',
        join_paths(meson.current_source_dir(), '..'),
        '-I',
        join_paths(meson.current_build_dir(), '..'),
        '-o',
        '@OUTPUT0@',
    ],
    depend_files: pxd_depfiles,
    depends: [pxd_deps, copy_py_in_buildir],
)


shared_library(
    '_builtins',
    builtins_c,
    dependencies : [libgodot, libpython],
    install_rpath: '$ORIGIN/lib',
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot', '_hazmat'),
)

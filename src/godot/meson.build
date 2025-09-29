##############################################################################
#                     Load subdirs (and their config)                        #
##############################################################################


subdir('hazmat')


##############################################################################
#                           Small fries to install                           #
##############################################################################


foreach src: ['__init__.py', 'classes.pxd', 'singletons.py', 'py.typed']
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
    output: 'utils.pyi',
    input: [
        generate_tmpl_base_input,
        files('utils.pyi.j2'),
    ],
    command: generate_tmpl_cmd,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)

custom_target(
    output: '_classes_api.py',
    input: [
        generate_tmpl_base_input,
        files('_classes_api.py.j2'),
    ],
    command: generate_tmpl_cmd,
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
            'builtins_pyx/method.pyx.j2',
            'builtins_pyx/operator.pyx.j2',
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


shared_library(
    'builtins',
    cbuiltins,
    gnu_symbol_visibility: 'hidden',  # Used by both clang & gcc (see https://gcc.gnu.org/wiki/Visibility)
    dependencies : [dep_godot, dep_python, dep_gdpy],
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


cclasses = custom_target(
    output : 'classes.c',
    input : [
        files('classes.pyx'),
        pxds_godot,
    ],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    classes_rpath = '$ORIGIN/../../..'
elif host_platform.startswith('macos')
    classes_rpath = '@loader_path/../../..'
else
    classes_rpath = ''
endif


shared_library(
    'classes',
    cclasses,
    gnu_symbol_visibility: 'hidden',  # Used by both clang & gcc (see https://gcc.gnu.org/wiki/Visibility)
    dependencies : [dep_godot, dep_python, dep_gdpy],
    install_rpath: classes_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


# utils.so
# └─ utils.c
#    ├─ gdextension_interface.pxd
#    │  └─ ...
#    └─ utils.pyx


pyxutils = custom_target(
    output: 'utils.pyx',
    input: [
        generate_tmpl_base_input,
        files(
            'utils.pyx.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


cutils = custom_target(
    output : 'utils.c',
    input : [pyxutils, pxds_godot],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    utils_rpath = '$ORIGIN/../../..'
elif host_platform.startswith('macos')
    utils_rpath = '@loader_path/../../..'
else
    utils_rpath = ''
endif


shared_library(
    'utils',
    cutils,
    gnu_symbol_visibility: 'hidden',  # Used by both clang & gcc (see https://gcc.gnu.org/wiki/Visibility)
    dependencies : [dep_godot, dep_python, dep_gdpy],
    install_rpath: utils_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)


# _lang.so
# └─ _lang.c
#    ├─ gdextension_interface.pxd
#    │  └─ ...
#    ├─ _lang_resource_format_loader.pxi
#    ├─ _lang_resource_format_saver.pxi
#    ├─ _lang_script_language.pxi
#    ├─ _lang_script.pxi
#    ├─ _lang_script_instance.pxi
#    ├─ _lang_tags.pxi
#    └─ _lang.pyx

preprocessed_lang_pxis = []
foreach pxi: [
    '_lang_resource_format_loader.pxi',
    '_lang_resource_format_saver.pxi',
    '_lang_script_language.pxi',
    '_lang_script.pxi',
    # Note `_lang_tags.pxi` & `_lang_script_instance.pxi` don't need preprocessing since they contain no class extension
]
    preprocessed_lang_pxis += custom_target(
        output: pxi,
        input: [
            join_paths(scripts_dir, 'gdextension_cython_preprocessor.py'),
            pxi,
        ],
        command: [python, '@INPUT0@', '@INPUT1@', '--output', '@OUTPUT@'],
    )
endforeach


c_lang = custom_target(
    output : '_lang.c',
    input : [
        files(
            '_lang.pyx',
            '_lang_script_instance.pxi',
            '_lang_tags.pxi',
        ),
        preprocessed_lang_pxis,
        pxds_godot
    ],
    command : cythonize_command,
)


if host_platform.startswith('linux')
    _lang_rpath = '$ORIGIN/../../..'
elif host_platform.startswith('macos')
    _lang_rpath = '@loader_path/../../..'
else
    _lang_rpath = ''
endif


shared_library(
    '_lang',
    c_lang,
    gnu_symbol_visibility: 'hidden',  # Used by both clang & gcc (see https://gcc.gnu.org/wiki/Visibility)
    dependencies : [dep_godot, dep_python, dep_gdpy],
    install_rpath: _lang_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot'),
)

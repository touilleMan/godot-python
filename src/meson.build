##############################################################################
#                       Code generation base config                          #
##############################################################################


# Input missing the template file
generate_tmpl_base_input = [
    join_paths(scripts_dir, 'generate_tmpl.py'),  # Must stay first !
    godot_extension_api_json,  # Must stay second !
    join_paths(scripts_dir, 'extension_api_parser/api.py'),
    join_paths(scripts_dir, 'extension_api_parser/builtins.py'),
    join_paths(scripts_dir, 'extension_api_parser/classes.py'),
    join_paths(scripts_dir, 'extension_api_parser/__init__.py'),
    join_paths(scripts_dir, 'extension_api_parser/__main__.py'),
    join_paths(scripts_dir, 'extension_api_parser/in_use.py'),
    join_paths(scripts_dir, 'extension_api_parser/type_spec.py'),
    join_paths(scripts_dir, 'extension_api_parser/utils.py'),
]


generate_tmpl_cmd = [
    python,
    '@INPUT0@',  # generate_tmpl.py
    '--input',
    '@INPUT1@',  # extension_api.json
    '--build-config',
    godot_build_config,
    '--output',
    '@OUTPUT0@',
]
if get_option('classes_sample')
    generate_tmpl_cmd += '--classes-sample'
endif


##############################################################################
#                              .pxd generation                               #
##############################################################################


# .pxd files are used for .pyx compilation, hence the generated .pxd must be
# created early on.
# However we cannot just put the generation code in the directory the .pxd should
# resides given this folder might be visited in the wrong order (for instance if
# `foo.pyx` imports `bar/spam.pxd` and `bar/spam.pyx` imports `../foo.pxd`).
# The "good" solution to this would be to be able to specify subfolder in output
# parameter, but this is not allowed by meson...
# So what we do here is:
# - generate the .pxd files here with it actual path encoded in it name (i.e.
#   `foo/bar/spam.pxd` becomes `foo#bar#spam.pxd`)
# - we use those .pxd to build our .pyx
# - in the sub directories, we also have custom rules to copy the generated
#   .pxd files in their expected location (only needed for the install step)
# see https://github.com/mesonbuild/meson/issues/2320#issuecomment-1147929155


# godot/hazmat/gdextension_interface.pxd
# └─ gdextension.h

# Convert the header file frome C to Cython
pxd_godot_hazmat_gdextension = custom_target(
    output: 'godot#hazmat#gdextension_interface.pxd',
    input: [
        join_paths(scripts_dir, 'generate_gdextension_interface_pxd.py'),
        join_paths(gdextension_path, 'godot/gdextension_interface.h')
    ],
    command: [python, '@INPUT0@', '--input', '@INPUT1@', '--output', '@OUTPUT@'],
)


# godot/hazmat/gdnative_ptrs.pxd
# └─ extension_api.json

pxd_godot_hazmat_gdnative_ptrs = custom_target(
    output: 'godot#hazmat#gdnative_ptrs.pxd',
    input: [
        generate_tmpl_base_input,
        files(
            'godot/hazmat/gdnative_ptrs.pxd.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


# godot/hazmat/gdapi.pxd
# └─ extension_api.json

pxd_godot_hazmat_gdapi = custom_target(
    output: 'godot#hazmat#gdapi.pxd',
    input: [
        generate_tmpl_base_input,
        files(
            'godot/hazmat/gdapi.pxd.j2',
            'godot/hazmat/gdapi_pxd/struct.pxd.j2',
            'godot/hazmat/gdapi_pxd/meth.pxd.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


# godot/builtins.pxd
# └─ extension_api.json


pxd_godot_builtins = custom_target(
    output: 'godot#builtins.pxd',
    input: [
        generate_tmpl_base_input,
        files(
            'godot/builtins.pxd.j2',
            'godot/builtins_pxd/class.pxd.j2',
            'godot/builtins_pxd/constructor.pxd.j2',
            'godot/builtins_pxd/conversion.pxd.j2',
            'godot/builtins_pxd/member.pxd.j2',
            'godot/builtins_pxd/method.pxd.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


# godot/classes.pxd
# └─ extension_api.json


pxd_godot_classes = custom_target(
    output: 'godot#classes.pxd',
    input: [
        generate_tmpl_base_input,
        files('godot/classes.pxd.j2'),
    ],
    command: generate_tmpl_cmd,
)


# Groups of pxds to simplify includes in pyx compilation


pxds_godot_hazmat = [
    pxd_godot_hazmat_gdextension,
    pxd_godot_hazmat_gdnative_ptrs,
    pxd_godot_hazmat_gdapi,
    files(
        'godot/hazmat/extension_class.pxd',
    )
]


pxds_godot = [
    pxds_godot_hazmat,
    pxd_godot_builtins,
    pxd_godot_classes,
]


##############################################################################
#              _pythonscript.c & _pythonscript_api.h generation              #
##############################################################################


preprocessed_pxis = []
foreach pxi: [
    '_pythonscript_extension_class_language.pxi',
    '_pythonscript_extension_class_script.pxi',
]
    preprocessed_pxis += custom_target(
        output: pxi,
        input: [
            join_paths(scripts_dir, 'gdextension_cython_preprocessor.py'),
            pxi,
        ],
        command: [python, '@INPUT0@', '@INPUT1@', '--output', '@OUTPUT@'],
    )
endforeach

# _pythonscript.c
# _pythonscript_api.h
# ├─ _pythonscript.pyx
# ├─ _pythonscript_editor.pxi
# ├─ _pythonscript_registration.pxi
# ├─ godot/hazmat/gdapi.pxd
# ├─ godot/builtins.pxd
# |  └─ ...
# └─ godot/hazmat/gdextension_interface.pxd
#    └─ ...


# `_pythonscript_api.h` is needed to compile `libpythonscript.so` (see below)
# Note we don't need to link `libpythonscript.so` against `_pythonscript.so`
# given `_pythonscript_api.h` contains a static inline functions that uses
# Python's import system to dynamically load `_pythonscript.so`


# `_pythonscript_api.h` is used to expose the Python callbacks used by `pythonscript.c`,
# hence this header is private and won't be provided in the release
c_pythonscript = custom_target('_pythonscript.c & _pythonscript.h & _pythonscript_api.h',
    output : ['_pythonscript.c', '_pythonscript_api.h'],
    input : [
        '_pythonscript.pyx',
        '_pythonscript_editor.pxi',
        preprocessed_pxis,
        pxds_godot
    ],
    command : cythonize_command,
)
h_pythonscript_api = c_pythonscript[1]  # Header for pythonscript.c
c_pythonscript = c_pythonscript[0]


##############################################################################
#                     libythonscript.so compilation                          #
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
    ['pythonscript.c', h_pythonscript_api],
    dependencies: [dep_godot, dep_python],
    install_rpath: lib_pythonscript_rpath,  # To find libpython
    install: true,
    install_dir: 'addons/pythonscript/' + host_platform,
)


# This dependency is used by all Cython modules to retreive the `pythonscript_gdapi`
# global variable that is declared as extern in `godot.hazmat.gdapi`
# Note we don't need to configure a rpath for Cython modules, this is because
# `libpythonscript.so` is responsible for initialiazing the Python interpreter
# and hence we are guaranteed it is already loaded when Cython modules kick in
dep_pythonscript = declare_dependency(
    link_with: lib_pythonscript,
)


##############################################################################
#          _pythonscript.pyx compilation (required by other .pyx)            #
##############################################################################


# _pythonscript.so
# ├─ libpythonscript.so
# |  └─ ...
# └─ _pythonscript.c
#    └─ _pythonscript.pyx
#       └─ ...


if host_platform.startswith('linux')
    lib__pythonscript_rpath = '$ORIGIN/../..'
elif host_platform.startswith('macos')
    lib__pythonscript_rpath = '@loader_path/../..'
else
    lib__pythonscript_rpath = ''
endif


# Cython's cdef inline methods are turned into static inline C functions that
# produced `defined but not used` errors, hence the `-Wno-unused-function`
# AutoPxd currently strip const qualifier when generating `gdextension_interface.pxd`,
# hence -Wno-discarded-qualifiers
if host_platform.startswith('windows')
    lib__pythonscript_c_args = []
else
    lib__pythonscript_c_args = ['-Wno-discarded-qualifiers', '-Wno-incompatible-pointer-types-discards-qualifiers', '-Wno-unused-function']
endif


lib__pythonscript = shared_library(
    '_pythonscript',
    c_pythonscript,
    c_args: lib__pythonscript_c_args,
    dependencies : [dep_godot, dep_python, dep_pythonscript],
    install_rpath: lib__pythonscript_rpath,  # To find libpython
    name_prefix: python_native_module_name_prefix,
    name_suffix: python_native_module_name_suffix,
    install: true,
    install_dir: python_site_packages_install_path,
)


##############################################################################
#                     Load subdirs (and their config)                        #
##############################################################################


subdir('godot')

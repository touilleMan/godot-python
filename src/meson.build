##############################################################################
#                           Small fries to install                           #
##############################################################################


install_subdir(
    'godot',
    install_dir: join_paths(python_site_packages_install_path),
)


##############################################################################
#                       Code generation base config                          #
##############################################################################


# List everything `generate_tmpl.py` needs to work, except the template file
# itself, as it is the only thing that changes between the different targets.
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
if get_option('builtins_sample')
    generate_tmpl_cmd += '--builtins-sample'
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


# godot/hazmat/gdptrs.pxd
# └─ extension_api.json

pxd_godot_hazmat_gdptrs = custom_target(
    output: 'godot#hazmat#gdptrs.pxd',
    input: [
        generate_tmpl_base_input,
        files(
            'godot/hazmat/gdptrs.pxd.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


# godot/hazmat/gdtypes.pxd
# └─ extension_api.json

pxd_godot_hazmat_gdtypes = custom_target(
    output: 'godot#hazmat#gdtypes.pxd',
    input: [
        generate_tmpl_base_input,
        files(
            'godot/hazmat/gdtypes.pxd.j2',
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
    pxd_godot_hazmat_gdptrs,
    pxd_godot_hazmat_gdtypes,
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
#              gdpy_gdextension_ptrs.c & generation                  #
##############################################################################


c_gdpy_gdextension_ptrs = custom_target(
    output: 'gdpy_gdextension_ptrs.c',
    input: [
        generate_tmpl_base_input,
        files(
            'gdpy_gdextension_ptrs.c.j2',
        ),
    ],
    command: generate_tmpl_cmd,
)


##############################################################################
#                     libythonscript.so compilation                          #
##############################################################################


# libgdpy.so
# ├─ gdpy.c
# ├─ gdpy_gdextension_ptrs.c
# └─ ...


if host_platform.startswith('linux')
    lib_gdpy_rpath = '$ORIGIN/lib'
elif host_platform.startswith('macos')
    lib_gdpy_rpath = '@loader_path/lib'
else
    lib_gdpy_rpath = ''
endif


lib_gdpy = shared_library(
    'gdpy',
    ['gdpy.c', c_gdpy_gdextension_ptrs],
    gnu_symbol_visibility: 'hidden',  # Used by both clang & gcc (see https://gcc.gnu.org/wiki/Visibility)
    dependencies: [dep_godot, dep_python],
    install_rpath: lib_gdpy_rpath,  # To find libpython
    install: true,
    install_dir: 'addons/gdpy/' + host_platform,
)


# This dependency is used by all Cython modules to retreive the `gdpy_gdapi`
# global variable that is declared as extern in `godot.hazmat.gdapi`
# Note we don't need to configure a rpath for Cython modules, this is because
# `libgdpy.so` is responsible for initialiazing the Python interpreter
# and hence we are guaranteed it is already loaded when Cython modules kick in
dep_gdpy = declare_dependency(
    link_with: lib_gdpy,
)


##############################################################################
#                     Load subdirs (and their config)                        #
##############################################################################


subdir('godot')

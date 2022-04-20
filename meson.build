project(
  'godot-python',
  'c',
  version : '0.50.0+dev',
  meson_version: '>=0.60.0',
  # warning_level=3 uses -Wpedantic that doesn't play nice with cython-generated code
  default_options : ['warning_level=2']
)

host_platform = '@0@-@1@'.format(host_machine.system(), host_machine.cpu_family())
if (
    host_platform != 'linux-x86_64'
    and host_platform != 'windows-x86'
    and host_platform != 'windows-x86_64'
    and host_platform != 'darwin-x86_64'
)
    error('Unsupported host platform: @0@'.format(host_platform))
endif

# We stick with Godot's platform naming
# Note darwin may refere to ios and osx (because it's sooo clever to designate
# two totally diferent things with the same name...) but we only support osx
if host_platform == 'darwin-x86_64'
    host_platform = 'osx-x86_64'
endif

python = find_program('python')
cython = find_program('cython')
cc = meson.get_compiler('c')


##############################################################################
#                             Python distrib                                 #
##############################################################################


cpython_distrib_version_major = get_option('cpython_distrib_version').split('.')[0]
cpython_distrib_version_minor = get_option('cpython_distrib_version').split('.')[1]

message('Fetching CPython v@0@ prebuild distrib...'.format(get_option('cpython_distrib_version')))
run_command(
    python,
    'scripts/python_distrib.py',
    'fetch_prebuild',
    '--host-platform', host_platform,
    '--cpython-version', get_option('cpython_distrib_version'),
    '--output-dir', meson.current_build_dir(),
    capture: true,
    check: true,
)

message('Generating CPython custom distrib from the prebuild...')
run_command(
    python,
    'scripts/python_distrib.py',
    'build_distrib',
    '--host-platform', host_platform,
    '--cpython-version', get_option('cpython_distrib_version'),
    '--output-dir', meson.current_build_dir(),
    '--compressed-stdlib',
    capture: true,
    check: true,
)

# We link against the prebuild but use the distrib at the runtime
python_prebuild_name = 'python_prebuild-@0@-@1@'.format(
    get_option('cpython_distrib_version'),
    host_platform,
)
python_prebuild_path = join_paths(meson.current_build_dir(), python_prebuild_name)
python_distrib_path = meson.current_build_dir() + 'python_distrib'

# Define the `libpython` dependency
if build_machine.system() == 'linux'
    libpython = declare_dependency(
        dependencies: cc.find_library(
            # e.g. python3.9
            'python@0@.@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor),
            dirs: join_paths(python_prebuild_path , 'python/install/lib')
        ),
        include_directories: [join_paths(python_prebuild_name, 'python/install/include/python3.9')],
    )
elif build_machine.system() == 'windows'
    libpython = declare_dependency(
        dependencies: cc.find_library(
            # e.g. python39
            'python@0@@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor),
            dirs: [
                # join_paths(python_prebuild_path , 'python/install'),
                join_paths(python_prebuild_path , 'python/install/libs'),
            ],
        ),
        include_directories: [join_paths(python_prebuild_name, 'python/install/include')],
    )
endif

# add_install_script(
#     python,
#     ['scripts/install_python_distrib.py',]
# )


##############################################################################
#                         Godot extension headers                            #
##############################################################################


godot_headers_path = join_paths(meson.project_source_root(), get_option('godot_headers'))

# On Windows `/MDd` flag (used by meson when `buildtype=debug`) defines `_DEBUG`,
# however this makes `python.h` (`pyconfig.h` actually) to consider we should link
# against `python39_d.lib`, but we only have `python39.lib` available...
add_global_arguments('-U_DEBUG', language : 'c')


# Retreive Godot version from the extension headers
# (This is done once at configure time)
godot_version_info = run_command(
    python,
    'scripts/extract_godot_version.py',
    '--godot-headers', godot_headers_path,
    capture: true,
    check: true,
).stdout().strip().split('\n')
godot_version_fullname = godot_version_info[0]
message('Godot extension headers version: @0@'.format(godot_version_fullname))

# Define the `libgodot` dependency
godot_version_major = godot_version_info[1]
godot_version_minor = godot_version_info[2]
libgodot = declare_dependency(
    compile_args: [
        '-DGODOT_VERSION_MAJOR=' + godot_version_major,
        '-DGODOT_VERSION_MINOR=' + godot_version_minor,
        # Don't use `include_directories` param to pass `godot_header_path`
        # given it is an absolute path
        '-I' + godot_headers_path,
    ],
)


##############################################################################
#                         Misc install stuff                                 #
##############################################################################


install_data(
    'misc/release_README.txt',
    install_dir: 'addons/pythonscript',
    rename: 'README.TXT',
)
install_data(
    'misc/release_LICENSE.txt',
    install_dir: 'addons/pythonscript',
    rename: 'LICENSE.TXT',
)
install_data(
    'misc/release_pythonscript.gdextension',
    rename: 'pythonscript.gdextension',
)


subdir('src')
subdir('tests')

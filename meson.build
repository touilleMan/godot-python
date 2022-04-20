project(
  'godot-python',
  'c',
  version : '0.50.0+dev',
  meson_version: '>=0.60.0',
  # warning_level=3 uses -Wpedantic that doesn't play nice with cython-generated code
  default_options : ['warning_level=2']
)


python = find_program('python')
cython = find_program('cython')
cc = meson.get_compiler('c')


##############################################################################
#                             Python distrib                                 #
##############################################################################


# Download&extract CPython prebuild archive
# (This is done once at configure time)
message('Fetching CPython v@0@ prebuild distrib'.format(get_option('cpython_distrib_version')))
run_command(
    python,
    'scripts/fetch_python_distrib.py',
    '--host-platform', host_machine.system() + '-' + host_machine.cpu_family(),
    '--cpython-version', get_option('cpython_distrib_version'),
    '--output-dir', meson.current_build_dir(),
    capture: true,
    check: true,
)

cpython_distrib_version_major = get_option('cpython_distrib_version').split('.')[0]
cpython_distrib_version_minor = get_option('cpython_distrib_version').split('.')[1]

# Define the `libpython` dependency
if build_machine.system() == 'linux'
    libpython = declare_dependency(
        dependencies: cc.find_library(
            # e.g. python3.9
            'python@0@.@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor),
            dirs: join_paths(meson.current_build_dir() , 'python/install/lib')
        ),
        include_directories: ['python/install/include/python3.9'],
    )
elif build_machine.system() == 'windows'
    libpython = declare_dependency(
        dependencies: cc.find_library(
            # e.g. python39
            'python@0@@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor),
            dirs: [
                # join_paths(meson.current_build_dir() , 'python/install'),
                join_paths(meson.current_build_dir() , 'python/install/libs'),
            ],
        ),
        include_directories: ['python/install/include'],
    )
endif


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


subdir('src')
subdir('tests')

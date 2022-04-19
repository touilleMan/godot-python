project(
  'godot-python',
  'c',
  version : '0.60.0',
  meson_version: '>=0.60.0',
  default_options : ['warning_level=3']
)

python = find_program('python')
cython = find_program('cython')


godot_headers_path = join_paths(meson.project_source_root(), get_option('godot_headers'))


# Download&extract CPython prebuild archive
# This is done once at configure time

message('Fetching cpython prebuild distrib')
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

cc = meson.get_compiler('c')

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
                join_paths(meson.current_build_dir() , 'python/install'),
                join_paths(meson.current_build_dir() , 'python/install/libs'),
            ],
        ),
        include_directories: ['python/install/include'],
    )
endif


subdir('pythonscript')

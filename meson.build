project(
    'godot-python',
    'c',
    version : '0.50.0+dev',
    meson_version: '>=0.61.0',
    default_options : [
        # warning_level=3 uses -Wpedantic that doesn't play nice with cython-generated code
        'warning_level=2',
        # Overwrite default prefix (e.g. /usr/local on linux), note installing is
        # always done with a --destdir given installing this project globally on
        # the system is meaningless
        'prefix=/',
        'c_std=c17',
    ]
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
autopxd = find_program('autopxd')
cc = meson.get_compiler('c')


##############################################################################
#                             Python distrib                                 #
##############################################################################


cpython_distrib_version_major = get_option('cpython_distrib_version').split('.')[0]
cpython_distrib_version_minor = get_option('cpython_distrib_version').split('.')[1]
# Version Minor.Major
cython_vmdm = '@0@.@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor)
# Version MinorMajor
cython_vmm = '@0@@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor)


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
python_distrib_path = join_paths(meson.current_build_dir(), 'python_distrib')
# Define the `libpython` dependency
if build_machine.system() == 'linux'
    libpython = declare_dependency(
        dependencies: cc.find_library(
            # e.g. python3.9
            'python@0@.@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor),
            dirs: join_paths(python_prebuild_path , 'python/install/lib')
        ),
        include_directories: [join_paths(python_prebuild_name, 'python/install/include/python@0@.@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor))],
    )
    # e.g. addons/pythonscript/linux-x86_64/lib/python3.9/site-packages
    python_site_packages_install_path = join_paths(
        'addons/pythonscript',
        host_platform,
        'lib/python@0@.@1@/site-packages'.format(cpython_distrib_version_major, cpython_distrib_version_minor)
    )
elif build_machine.system() == 'windows'
    libpython = declare_dependency(
        dependencies: cc.find_library(
            # e.g. python39
            'python@0@@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor),
            dirs: [
                join_paths(python_prebuild_path , 'python/install/libs'),
            ],
        ),
        include_directories: [join_paths(python_prebuild_name, 'python/install/include')],
    )
    # e.g. addons/pythonscript/windows-x86_64/Lib/site-packages
    python_site_packages_install_path = join_paths(
        'addons/pythonscript',
        host_platform,
        'Lib/site-packages'
    )
endif


install_subdir(
    python_distrib_path,
    install_dir: join_paths('addons/pythonscript', host_platform),
    strip_directory: true,
)
if build_machine.system() == 'linux'
    # TODO: Bug in meson prevent symlink from being correctly copied, so we do it by hand
    # see: https://github.com/mesonbuild/meson/issues/9233
    mm = '@0@.@1@'.format(cpython_distrib_version_major, cpython_distrib_version_minor)
    bad_links = [
        # (<parent dir>, <symlink name>, <target name>)
        ['bin', '2to3', '2to3-@0@'.format(mm)],
        ['bin', 'idle3', 'idle@0@'.format(mm)],
        ['bin', 'pydoc3', 'pydoc@0@'.format(mm)],
        ['bin', 'python3', 'python@0@'.format(mm)],
        ['bin', 'python3-config', 'python@0@-config'.format(mm)],
        ['lib', 'libpython@0@.so'.format(mm), 'libpython@0@.so.1.0'.format(mm)],
    ]
    foreach x: bad_links
        parent_dir = x[0]
        symlink_name = x[1]
        target_name = x[2]
        run_command(
            python,
            '-c',
            'from os import unlink; unlink("@0@")'.format(
                join_paths(
                    python_distrib_path,
                    parent_dir,
                    symlink_name,
                )
            ),
            check: false,  # Ignore error raised by unlink if the file doesn't exists
            capture: true,
        )
        install_symlink(
            symlink_name,
            install_dir: join_paths('addons/pythonscript', host_platform, parent_dir),
            pointing_to: target_name,
        )
    endforeach
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
message('Detected Godot extension version: @0@'.format(godot_version_fullname))

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

# Convert the header file frome C to Cython
gdnative_interface_pxd = custom_target('gdnative_interface.pxd',
    output: 'gdnative_interface.pxd',
    input: join_paths(godot_headers_path, 'godot/gdnative_interface.h'),
    command: [autopxd, '@INPUT@', '@OUTPUT@'],
    # We provide this file as part of the distribution so that end user can
    # write Cython module with low level access to Godot API
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot/_hazmat'),
)


##############################################################################
#                         Misc install stuff                                 #
##############################################################################


install_data(
    'LICENSE.txt',
    install_dir: 'addons/pythonscript',
)
# Add date&version info to README before installing it
custom_target(
    'release_readme',
    command: [
        python,
        '-c',
        '''
from datetime import date
src = open("@INPUT0@", mode="r", encoding="utf8").read()
out = src.format(version="@0@", date=str(date.today()))
open("@OUTPUT0@", mode="w", encoding="utf8").write(out)
'''.format(meson.project_version())
    ],
    output: ['README.txt'],
    input: ['misc/release_README.txt'],
    install: true,
    install_dir: '.',
)
install_data(
    'misc/release_pythonscript.gdextension',
    install_dir: '.',
    rename: 'pythonscript.gdextension',
)


subdir('src')


##############################################################################
#                             Config summary                                 #
##############################################################################


summary(
    {
        'Godot extension version': godot_version_fullname,
        'Embedded Python version': get_option('cpython_distrib_version'),
    }
)

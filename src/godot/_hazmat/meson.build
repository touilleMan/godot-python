# gdnative_interface.pxd
#  └─ gdnative_interface.h


# Convert the header file frome C to Cython
gdnative_interface_pxd = custom_target('generate gdnative_interface.pxd',
    output: 'gdnative_interface.pxd',
    input: [
        join_paths(scripts_dir, 'generate_gdnative_interface_pxd.py'),
        join_paths(godot_headers_path, 'godot/gdnative_interface.h')
    ],
    command: [python, '@INPUT0@', '--input', '@INPUT1@', '--output', '@OUTPUT@'],
    # We provide this file as part of the distribution so that end user can
    # write Cython module with low level access to Godot API
    install: true,
    install_dir: join_paths(python_site_packages_install_path, 'godot/_hazmat'),
)

pxd_deps += gdnative_interface_pxd
pxd_depfiles += files('gdapi.pxd')

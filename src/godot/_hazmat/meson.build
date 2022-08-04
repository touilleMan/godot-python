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

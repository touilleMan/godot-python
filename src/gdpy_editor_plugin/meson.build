# Add version info before installing it
custom_target(
    'release_plugin.cfg',
    command: [
        python,
        '-c',
        '''
src = open("@INPUT0@", mode="r", encoding="utf8").read()
out = src.format(version="@0@")
open("@OUTPUT0@", mode="w", encoding="utf8").write(out)
'''.format(meson.project_version())
    ],
    output: ['plugin.cfg'],
    input: ['plugin.cfg'],
    install: true,
    install_dir: 'addons/gdpy_editor_plugin',
)


install_data(
    'gdpy_editor_plugin.gd',
    install_dir: 'addons/gdpy_editor_plugin',
)


install_data(
    'gdpy_editor_plugin.gd.uid',
    install_dir: 'addons/gdpy_editor_plugin',
)

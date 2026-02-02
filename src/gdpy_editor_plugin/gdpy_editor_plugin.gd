@tool
extends EditorPlugin

const TEXTFILE_EXTENSIONS_SETTING := "docks/filesystem/textfile_extensions"
const PYTHON_EXTENSIONS := ["py", "pyi", "pyx", "pxd", "pxi"]
const PYCACHE_DIR := "__pycache__"
const GDIGNORE_FILE := ".gdignore"


func _enter_tree() -> void:
	var needs_rescan := false
	needs_rescan = _register_python_extensions() or needs_rescan
	needs_rescan = _ignore_pycache_folders("res://") or needs_rescan
	if needs_rescan:
		EditorInterface.get_resource_filesystem().scan()


func _exit_tree() -> void:
	pass


func _register_python_extensions() -> bool:
	var settings := EditorInterface.get_editor_settings()
	var current_extensions: String = settings.get_setting(TEXTFILE_EXTENSIONS_SETTING)

	var existing := {}
	for ext in current_extensions.split(",", false):
		existing[ext.strip_edges()] = true

	var to_add: PackedStringArray = []
	for ext in PYTHON_EXTENSIONS:
		if not existing.has(ext):
			to_add.append(ext)

	if to_add.is_empty():
		return false

	var new_extensions := current_extensions
	for ext in to_add:
		if new_extensions.is_empty():
			new_extensions = ext
		else:
			new_extensions += "," + ext

	settings.set_setting(TEXTFILE_EXTENSIONS_SETTING, new_extensions)
	return true


func _ignore_pycache_folders(path: String) -> bool:
	var dir := DirAccess.open(path)
	if dir == null:
		return false

	var changed := false
	dir.list_dir_begin()
	var file_name := dir.get_next()
	while file_name != "":
		if dir.current_is_dir() and not file_name.begins_with("."):
			var full_path := path.path_join(file_name)
			if file_name == PYCACHE_DIR:
				if _create_gdignore(full_path):
					changed = true
			else:
				if _ignore_pycache_folders(full_path):
					changed = true
		file_name = dir.get_next()
	dir.list_dir_end()
	return changed


func _create_gdignore(pycache_path: String) -> bool:
	var gdignore_path := pycache_path.path_join(GDIGNORE_FILE)
	if FileAccess.file_exists(gdignore_path):
		return false

	var file := FileAccess.open(gdignore_path, FileAccess.WRITE)
	if file == null:
		push_warning("Failed to create %s" % gdignore_path)
		return false
	file.close()
	return true

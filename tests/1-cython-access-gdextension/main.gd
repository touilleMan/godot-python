const PROJECT_SETTING_NAME = "my/result"

func _ready():
	# The Cython gdextension module should have created this project setting
	var project_setting_value = ProjectSettings.get_setting(PROJECT_SETTING_NAME)
	if project_setting_value != "all_good":
		printerr("Missing/invalid project setting `{}`".format(project_setting_value))
		self.get_tree().quit(2)
	else:
		self.get_tree().quit(0)
